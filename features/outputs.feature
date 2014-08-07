Feature: Printing different output formats
  In order to visualise the QC results
  The auto-qc tool can generate different output formats

  Scenario Outline: Generating YAML output
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: <variable>
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.0.0
     thresholds:
     -
       - <operator>
       - :object_1/metric_1/value
       - <literal>
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --yaml-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      evaluation:
      - - <operator>
        - <variable>
        - <literal>
      metadata:
        version:
          auto-qc: 1.0.0
      state:
        fail: <status>
      thresholds:
      - - <operator>
        - :object_1/metric_1/value
        - <literal>

      """

  Examples: Operators
      | variable | operator     | literal | status |
      | 1        | greater_than | 0       | true   |
      | 1        | greater_than | 2       | false  |

  Scenario: Generating text readable output for a failing metric
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: 1
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.0.0
     thresholds:
     -
       - less_than
       - 2
       - :object_1/metric_1/value
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --text-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      Status: FAIL

                Failure   Actual

      Test 1:       < 2        1   FAIL

      Auto QC Version: 1.0.0

      """

  Scenario: Generating text readable output for a multiple metrics
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: 1
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.0.0
     thresholds:
     -
       - less_than
       - 2
       - :object_1/metric_1/value
     -
       - greater_than
       - 2
       - :object_1/metric_1/value
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --text-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      Status: FAIL

                                Failure   Actual

      :object_1/metric_1/value      < 2        1   FAIL
      :object_1/metric_1/value      > 2        1

      Auto QC Version: 1.0.0

      """

  Scenario: Generating text readable output for a passing nested metric
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: 1
         metric_2:
           value: 2
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.0.0
     thresholds:
     -
       - and
       -
         - less_than
         - 2
         - :object_1/metric_1/value
       -
         - greater_than
         - 2
         - :object_1/metric_2/value
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --text-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      Status: PASS

                                  Failure   Actual

      AND:
        :object_1/metric_1/value      < 2        1   F
        :object_2/metric_2/value      > 2        1

      Auto QC Version: 1.0.0

      """

  Scenario: Generating text readable output for a failing nested metric
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: 1
         metric_2:
           value: 2
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.0.0
     thresholds:
     -
       - or
       -
         - less_than
         - 2
         - :object_1/metric_1/value
       -
         - greater_than
         - 2
         - :object_1/metric_1/value
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --text-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      Status: FAIL

                                  Failure   Actual

      OR:                                            FAIL
        :object_1/metric_1/value      < 2        1   F
        :object_2/metric_2/value      > 2        1

      Auto QC Version: 1.0.0

      """
