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
