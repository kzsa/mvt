# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2023 The MVT Authors.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging
from typing import Optional

from mvt.common.utils import convert_datetime_to_iso
from .base import BugReportModule
from mvt.android.artifacts.file_timestamps import FileTimestampsArtifact


class BugReportTimestamps(FileTimestampsArtifact, BugReportModule):
    """This module extracts records from battery daily updates."""

    slug = "bugreport_timestamps"

    def __init__(
        self,
        file_path: Optional[str] = None,
        target_path: Optional[str] = None,
        results_path: Optional[str] = None,
        module_options: Optional[dict] = None,
        log: logging.Logger = logging.getLogger(__name__),
        results: Optional[list] = None,
    ) -> None:
        super().__init__(
            file_path=file_path,
            target_path=target_path,
            results_path=results_path,
            module_options=module_options,
            log=log,
            results=results,
        )

    def run(self) -> None:
        filesystem_files = self._get_files_by_pattern("FS/*")

        self.results = []
        for file in filesystem_files:
            # Only the modification time is available in the zip file metadata.
            # The timezone is the local timezone of the machine the phone.
            modification_time = self._get_file_modification_time(file)
            self.results.append(
                {
                    "path": file,
                    "modified_time": convert_datetime_to_iso(modification_time),
                }
            )

        self.log.info(
            "Extracted a total of %d filesystem timestamps from bugreport.",
            len(self.results),
        )
