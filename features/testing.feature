Feature: Using the auto-qc tool
  In order to determine whether a sample passes QC
  The auto-qc tool can be used to
  Test quality thresholds

  Scenario Outline: Threshold operators
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
         auto-qc: 1.2.1
     thresholds:
     -
       - <operator>
       - :object_1/metric_1/value
       - <literal>
     """
    When I run the command "../bin/auto-qc" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should contain:
      """
      <result>

      """

  Examples: Operators
      | variable | operator           | literal      | result |
      | 1        | greater_than       | 0            | FAIL   |
      | 1        | greater_than       | 2            | PASS   |
      | 1        | less_than          | 2            | FAIL   |
      | 1        | less_than          | 0            | PASS   |
      | 1        | greater_equal_than | 0            | FAIL   |
      | 1        | greater_equal_than | 2            | PASS   |
      | 1        | less_equal_than    | 2            | FAIL   |
      | 1        | less_equal_than    | 0            | PASS   |
      | 1        | greater_equal_than | 1            | FAIL   |
      | 1        | less_equal_than    | 1            | FAIL   |
      | True     | and                | True         | FAIL   |
      | False    | and                | True         | PASS   |
      | True     | and                | False        | PASS   |
      | False    | and                | False        | PASS   |
      | True     | or                 | True         | FAIL   |
      | False    | or                 | True         | FAIL   |
      | True     | or                 | False        | FAIL   |
      | False    | or                 | False        | PASS   |
      | 1        | not_equals         | 1            | PASS   |
      | 2        | not_equals         | 1            | FAIL   |
      | 1        | equals             | 1            | FAIL   |
      | 2        | equals             | 1            | PASS   |
      | A        | is_in              | [list, A, B] | FAIL   |
      | C        | is_in              | [list, A, B] | PASS   |
      | A        | is_not_in          | [list, A, B] | PASS   |
      | C        | is_not_in          | [list, A, B] | FAIL   |

  Scenario Outline: Multiple thresholds
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: <var_1>
     - analysis: object_2
       outputs:
         metric_2:
           value: <var_2>
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.2.1
     thresholds:
     - [greater_than, ':object_1/metric_1/value', <lit_1>]
     - [greater_than, ':object_2/metric_2/value', <lit_2>]
     """
    When I run the command "../bin/auto-qc" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should contain:
      """
      <result>

      """

  Examples: Operators
      | var_1 | lit_1 | var_2 | lit_2 | result |
      | 1     | 0     | 1     | 0     | FAIL   |
      | 1     | 0     | 0     | 1     | FAIL   |
      | 0     | 1     | 1     | 0     | FAIL   |
      | 0     | 1     | 0     | 1     | PASS   |

  Scenario Outline: Nested thresholds
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: <var_1>
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.2.1
     thresholds:
     -
       - and
       -
         - greater_than
         - :object_1/metric_1/value
         - <lit_1>
       -
         - greater_than
         - :object_1/metric_1/value
         - <lit_2>
     """
    When I run the command "../bin/auto-qc" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should contain:
      """
      <result>

      """

  Examples: Operators
      | var_1 | lit_1 | lit_2 | result |
      | 1     | 0     | 0     | FAIL   |
      | 1     | 0     | 1     | PASS   |
      | 1     | 1     | 0     | PASS   |
      | 1     | 1     | 1     | PASS   |

  Scenario: A library passing on insert size
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: insert_size
       outputs:
         metrics:
           mode: 198
     - analysis: library_type
       outputs:
         protocol: Ultra-Low Input (DNA)
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.2.1
     thresholds:
     -
       - and
       -
         - less_than
         - :insert_size/metrics/mode
         - 200
       -
         - not_equals
         - :library_type/protocol
         - Ultra-Low Input (DNA)
     """
    When I run the command "../bin/auto-qc" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should contain:
      """
      PASS

      """

  Scenario: A library failing on insert size
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: insert_size
       outputs:
         metrics:
           mode: 198
     - analysis: library_type
       outputs:
         protocol: Standard
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 1.2.1
     thresholds:
     -
       - and
       -
         - less_than
         - :insert_size/metrics/mode
         - 200
       -
         - not_equals
         - :library_type/protocol
         - Ultra-Low Input (DNA)
     """
    When I run the command "../bin/auto-qc" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should contain:
      """
      FAIL

      """
