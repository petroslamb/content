# Scenario

A coding agent fixes a serializer bug where a `0%` discount loses its label. The run reproduces the failure, inspects the serializer and test file, makes one narrow patch, reruns the target regression and the full suite, and stops before merge.
