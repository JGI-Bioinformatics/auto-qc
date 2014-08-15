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

  Scenario Outline: Using different text format operators
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
       - <operator>
       - :object_1/metric_1/value
       - 2
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --text-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should contain:
      """
      <output> 2

      """

  Examples: Operators
      | operator     | output |
      | greater_than | >      |
      | less_than    | <      |
      | equals       | ==     |
      | not_equals   | =/=    |


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
       - greater_than
       - :object_1/metric_1/value
       - 2
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

                                 Failure At   Actual

      :object_1/metric_1/value          > 2        1

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
       - :object_1/metric_1/value
       - 2
     -
       - greater_than
       - :object_1/metric_1/value
       - 2
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

                                 Failure At   Actual

      :object_1/metric_1/value          < 2        1   FAIL
      :object_1/metric_1/value          > 2        1

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
           value: 1
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
         - :object_1/metric_1/value
         - 2
       -
         - greater_than
         - :object_1/metric_2/value
         - 2
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

                                   Failure At   Actual

      AND:
        :object_1/metric_1/value          < 2        1   FAIL
        :object_1/metric_2/value          > 2        1

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
         - :object_1/metric_1/value
         - 2
       -
         - greater_than
         - :object_1/metric_2/value
         - 2
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

                                   Failure At   Actual

      OR:                                                FAIL
        :object_1/metric_1/value          < 2        1   FAIL
        :object_1/metric_2/value          > 2        2

      Auto QC Version: 1.0.0

      """

  Scenario: Generating text readable output for a long list metric
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: A
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.0.0
     thresholds:
     -
       - is_in
       - :object_1/metric_1/value
       - [list, A, B, C, D, E, F, G]
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

                                           Failure At   Actual

      :object_1/metric_1/value   is in [A, B, C, ...]        A   FAIL

      Auto QC Version: 1.0.0

      """
