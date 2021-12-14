# Easy statistics of each sentiment
from deephaven import Aggregation as agg, as_list

averages = result.aggBy(as_list([agg.AggAvg("Positive", "Negative", "Neutral", "Compound")]))
medians = result.aggBy(as_list([agg.AggMed("Positive", "Negative", "Neutral", "Compound")]))
deviations = result.aggBy(as_list([agg.AggStd("Positive", "Negative", "Neutral", "Compound")]))

# Positive percent
positive_percent = result.update("PositiveCount = Positive > 0 ? 1 : 0")\
    .aggBy(as_list([agg.AggSum("PositiveCount"), agg.AggCount("TotalCount")]))\
    .update("PositivePercent = PositiveCount / TotalCount")
