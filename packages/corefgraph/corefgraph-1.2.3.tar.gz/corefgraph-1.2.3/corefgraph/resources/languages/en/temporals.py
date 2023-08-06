# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from corefgraph.resources.lambdas import list_checker, equality_checker, matcher, fail

temporals = list_checker(("second", "minute", "hour", "day", "week", "month", "year", "decade", "century", "millennium",
      "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "now",
      "yesterday", "tomorrow", "age", "time", "era", "epoch", "morning", "evening", "day", "night", "noon", "afternoon",
      "semester", "trimester", "quarter", "term", "winter", "spring", "summer", "fall", "autumn", "season",
      "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
      "december"))