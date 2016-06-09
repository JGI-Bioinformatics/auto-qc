# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## 2.0.0

### Changed

  * Each threshold file entry must have associated metadata. This metadata
    includes the name of the test and pass/fail messages. This is used to
    generate human readable output with more relevant information as the
    analyst can write the QC pass/fail messages themselves rather than less
    readable manchine generated output. This text output is available via the
    `--text-output` flag.

  * The threshold file tests must now must all evaluate to TRUE for a pass.
    This contrasts with the 1.x version where all thresholds must evaluate to
    FALSE for a pass. This means the threshold file is now written as a series
    of statments describing how the sequence data should be to considered as
    passing QC.

  * Removed namespacing of analyses in the analysis file. The analysis file is
    now a dictionary with the fields `data` and `metadata`. The field `data` is
    a dictionary containing a the required metrics to do QC.
