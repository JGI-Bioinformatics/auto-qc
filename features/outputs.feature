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
      metadata:
        version:
          auto-qc: 1.0.0
      status:
        fail: <status>
      thresholds:
      -
        - <operator>
        - :object_1/metric_1/value
        - <literal>
      evaluation:
      -
        - <operator>
        - <variable>
        - <literal>

      """

  Examples: Operators
      | variable | operator     | literal | status |
      | 1        | greater_than | 0       | true   |
      | 1        | greater_than | 2       | false  |
