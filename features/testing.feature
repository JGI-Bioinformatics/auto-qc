Feature: Using the auto-qc tool
  In order to determine whether a sample passes QC
  The auto-qc tool can be used to
  Test quality thresholds

  Scenario Outline: Using different comparison operators
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
         auto-qc: 2.0.0
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
      | variable | operator | literal      | result |
      | 1        | '>'      | 0            | PASS   |
      | 1        | '<'      | 2            | PASS   |
      | 1        | '>'      | 2            | FAIL   |
      | 1        | '<'      | 0            | FAIL   |
      | 1        | '<='     | 0            | FAIL   |
      | 1        | '>='     | 0            | PASS   |
      | 1        | '<='     | 1            | PASS   |
      | 1        | '>='     | 1            | PASS   |
      | True     | and      | True         | PASS   |
      | False    | and      | True         | FAIL   |
      | True     | and      | False        | FAIL   |
      | False    | and      | False        | FAIL   |
      | True     | or       | True         | PASS   |
      | False    | or       | True         | PASS   |
      | True     | or       | False        | PASS   |
      | False    | or       | False        | FAIL   |
      | 1        | '!='     | 1            | FAIL   |
      | 2        | '!='     | 1            | PASS   |
      | 1        | '=='     | 1            | PASS   |
      | 2        | '=='     | 1            | FAIL   |
      | A        | in       | [list, A, B] | PASS   |
      | C        | in       | [list, A, B] | FAIL   |
      | A        | not_in   | [list, A, B] | FAIL   |
      | C        | not_in   | [list, A, B] | PASS   |


  Scenario: Using the unary not operator
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: true
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 2.0.0
     thresholds:
     -
       - not
       - :object_1/metric_1/value
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

  Scenario Outline: Testing multiple different thresholds
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
         auto-qc: 2.0.0
     thresholds:
     - ['>', ':object_1/metric_1/value', <lit_1>]
     - ['>', ':object_2/metric_2/value', <lit_2>]
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
      | 1     | 0     | 1     | 0     | PASS   |
      | 1     | 0     | 0     | 1     | FAIL   |
      | 0     | 1     | 1     | 0     | FAIL   |
      | 0     | 1     | 0     | 1     | FAIL   |

  Scenario Outline: Using nested thresholds
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
         auto-qc: 2.0.0
     thresholds:
     -
       - and
       -
         - '>'
         - :object_1/metric_1/value
         - <lit_1>
       -
         - '>'
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
      | 1     | 0     | 0     | PASS   |
      | 1     | 0     | 1     | FAIL   |
      | 1     | 1     | 0     | FAIL   |
      | 1     | 1     | 1     | FAIL   |

  Scenario: Using a doc string to name the threshold
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: 2
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 2.0.0
     thresholds:
     -
       - name: "My QC threshold"
       - '>'
       - :object_1/metric_1/value
       - 1
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
