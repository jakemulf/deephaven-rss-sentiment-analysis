# Simple statistics of each sentiment
from deephaven import Aggregation as agg, as_list

built_in_sia_all_averages = built_in_sia_all.aggBy(as_list([agg.AggAvg("Positive", "Negative", "Neutral", "Compound")]))
built_in_sia_all_medians = built_in_sia_all.aggBy(as_list([agg.AggMed("Positive", "Negative", "Neutral", "Compound")]))
built_in_sia_all_deviations = built_in_sia_all.aggBy(as_list([agg.AggStd("Positive", "Negative", "Neutral", "Compound")]))

# Positive percent of built in analysis
built_in_sia_all_positive_percent = built_in_sia_all.update("PositiveCount = Positive > Negative ? 1 : 0")\
    .aggBy(as_list([agg.AggSum("PositiveCount"), agg.AggCount("TotalCount")]))\
    .update("PositivePercent = PositiveCount / TotalCount")

# Positive percent of custom analysis
custom_sia_all_positive_percent = custom_sia_all.update("PositiveCount = Sentiment.equals(`positive`)")\
    .aggBy(as_list([agg.AggSum("PositiveCount"), agg.AggCount("TotalCount")]))\
    .update("PositivePercent = PositiveCount / TotalCount")

# Join 2 tables on the unique datetime and sentence combination
all_joined = built_in_sia_all.join(custom_sia_all, "Datetime, Sentence")
