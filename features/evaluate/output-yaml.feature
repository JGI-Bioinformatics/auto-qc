Feature: Using the auto-qc tool
  In order to determine whether a sample passes QC
  The auto-qc tool can be used to
  Generate an output YAML containing the results of the evaluation

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
         auto-qc: 1.0.0
     thresholds:
     -
       - <operator>
       - :object_1/metric_1/value
       - <literal>
     """
    When I run the command "../bin/auto-qc-evaluate" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the YAML-format standard out should equal:
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
      | variable | operator     | literal      | status |
      | 1        | greater_than | 0            | true   |
      | 1        | greater_than | 2            | false  |
      | 1        | less_than    | 2            | true   |
      | 1        | less_than    | 0            | false  |
      | true     | and          | true         | true   |
      | false    | and          | true         | false  |
      | true     | and          | false        | false  |
      | false    | and          | false        | false  |
      | true     | or           | true         | true   |
      | false    | or           | true         | true   |
      | true     | or           | false        | true   |
      | false    | or           | false        | false  |
      | 1        | not_equals   | 1            | false  |
      | 2        | not_equals   | 1            | true   |
      | 1        | equals       | 1            | true   |
      | 2        | equals       | 1            | false  |
      | A        | is_in        | [list, A, B] | true   |
      | C        | is_in        | [list, A, B] | false  |
      | A        | is_not_in    | [list, A, B] | false  |
      | C        | is_not_in    | [list, A, B] | true   |

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
         auto-qc: 1.0.0
     thresholds:
     - [greater_than, ':object_1/metric_1/value', <lit_1>]
     - [greater_than, ':object_2/metric_2/value', <lit_2>]
     """
    When I run the command "../bin/auto-qc-evaluate" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the YAML-format standard out should equal:
      """
      evaluation:
      - - greater_than
        - var_1
        - lit_1
      - - greater_than
        - var_2
        - lit_2
      metadata:
        version:
          auto-qc: 1.0.0
      state:
        fail: <status>
      thresholds:
      - - greater_than
        - :object_1/metric_1/value
        - lit_1
      - - greater_than
        - :object_2/metric_2/value
        - lit_2

      """

  Examples: Operators
      | var_1 | lit_1 | var_2 | lit_2 | status |
      | 1     | 0     | 1     | 0     | true   |
      | 1     | 0     | 0     | 1     | true   |
      | 0     | 1     | 1     | 0     | true   |
      | 0     | 1     | 0     | 1     | false  |

  Scenario Outline: Nested thresholds
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
         auto-qc: 1.0.0
     thresholds:
     - - and
       - [greater_than, ':object_1/metric_1/value', <lit_1>]
       - [greater_than, ':object_2/metric_2/value', <lit_2>]
     """
    When I run the command "../bin/auto-qc-evaluate" with the arguments:
       | key              | value         |
       | --analysis-file  | analysis.yml  |
       | --threshold-file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the YAML-format standard out should equal:
      """
      evaluation:
      -
        - and
        - - greater_than
          - var_1
          - lit_1
        - - greater_than
          - var_2
          - lit_2
      metadata:
        version:
          auto-qc: 1.0.0
      state:
        fail: <status>
      thresholds:
      - - and
        - [greater_than, ':object_1/metric_1/value', <lit_1>]
        - [greater_than, ':object_2/metric_2/value', <lit_2>]

      """

  Examples: Operators
      | var_1 | lit_1 | var_2 | lit_2 | status |
      | 1     | 0     | 1     | 0     | true   |
      | 1     | 0     | 0     | 1     | true   |
      | 0     | 1     | 1     | 0     | true   |
      | 0     | 1     | 0     | 1     | false  |
