# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## 2.0.0

### Changed

  * The threshold file tests must now must all evaluate to TRUE for a pass.
    This contrasts with the 1.x version where all thresholds must evaluate to
    FALSE for a pass. This means the threshold file is now written as a series
    of statments describing how the sequence data should be to considered as
    passing QC.
