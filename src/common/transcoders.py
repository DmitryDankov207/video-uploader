import logging
import math
import os
from pathlib import Path

from ffmpy import FFmpeg, FFprobe

CURRENT_DIR = Path(__file__).resolve().parent

logger = logging.getLogger(__name__)


class TooLargeFileException(ValueError):
    """
    Raise when video is too large to compress under 7Mb.
    """


class VideoTranscoder:
    """
    Compress image, generate thumbnail and gif.
    Could be used as a context manager.
    """

    DIMENSION = '576*1024'
    SIZE_LIMIT = 56_000_000  # 7Mb
    BITRATE_REDUCE_STEP = 100_000

    def __init__(self, base_filename: str, content: bytes) -> None:
        self.base_filename = base_filename
        self._content = content
        self._bitrate: int = 0

        # Helper files.
        self.input_filepath = f'{self.base_filename}.mp4'
        self._duration_filepath = f'{self.base_filename}-duration.txt'

        # Output files.
        self.compressed_filepath = f'{self.base_filename}-compressed.mp4'
        self.thumbnail_filepath = f'{self.base_filename}.jpg'
        self.gif_filepath = f'{self.base_filename}.gif'

        with open(self.input_filepath, 'wb') as f:
            f.write(content)

        self._fill_output_files()

    def __enter__(self) -> 'VideoTranscoder':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        self.delete_files()

    def calculate_bitrate(self) -> None:
        self._bitrate = math.ceil(self.SIZE_LIMIT / self.duration)
        logger.info(f'Bitrate is {self._bitrate}')

    @property
    def duration(self) -> int:
        with open(self._duration_filepath, 'w') as f:
            probe_args = '-show_entries format=duration -v quiet -of csv="p=0"'
            FFprobe(inputs={self.input_filepath: probe_args}).run(stdout=f)

        with open(self._duration_filepath, 'r') as f:
            duration = float(f.read())
            logger.info(f'Durarion is {duration}')
            return math.ceil(duration)

    def delete_files(self) -> None:
        self._delete_file(self.input_filepath)
        self._delete_file(self.compressed_filepath)
        self._delete_file(self.thumbnail_filepath)
        self._delete_file(self.gif_filepath)
        self._delete_file(self._duration_filepath)
        logger.info(
            'All temporary files with '
            f'base_filename={self.base_filename} deleted.'
        )

    def _fill_output_files(self) -> None:
        """
        Fill output files with ffmpeg generated data.
        """
        self._fill_compressed_file(self.input_filepath)

        FFmpeg(
            inputs={str(self.compressed_filepath): None},
            outputs={
                str(self.thumbnail_filepath): '-frames:v 1',
                str(self.gif_filepath): '-t 2',
            },
        ).run()

    def _fill_compressed_file(self, reduce_filepath: str) -> None:
        """
        Change video dimension.
        Reduce video bitrate if it needed.
        Write result in output file.

        :param reduce_filepath: Filepath to reduce bitrate.
        :return: No return value.
        """
        if self._size_limit_exceeded(reduce_filepath):
            if self._bitrate == 0:
                self.calculate_bitrate()
            if self._bitrate > self.BITRATE_REDUCE_STEP:
                self._bitrate -= self.BITRATE_REDUCE_STEP
            else:
                raise TooLargeFileException
            compress_args = f'-vf "scale={self.DIMENSION}" -b {self._bitrate}'
        else:
            compress_args = f'-vf "scale={self.DIMENSION}"'

        FFmpeg(
            inputs={self.input_filepath: None},
            outputs={self.compressed_filepath: compress_args},
        ).run()

        # If Video is larger than 7Mb, bitrate should be reduced.
        if self._size_limit_exceeded(self.compressed_filepath):
            self._delete_file(self.compressed_filepath)
            self._fill_compressed_file(
                reduce_filepath=self.compressed_filepath
            )

    def _size_limit_exceeded(self, filepath: str) -> bool:
        input_size = os.path.getsize(filepath) * 8  # Size in bits.
        return input_size > self.SIZE_LIMIT

    @staticmethod
    def _delete_file(filepath: str) -> None:
        if os.path.exists(filepath):
            os.remove(filepath)
