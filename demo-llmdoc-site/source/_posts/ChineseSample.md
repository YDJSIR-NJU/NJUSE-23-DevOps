---
title: ChineseSample
date: 2023-11-24 16:29:03
tags:
- test-spring
---

# PR-34 simple

> PR地址：https://git.nju.edu.cn/HongZe/test-spring/-/merge_requests/34

生成时间：11月 21, 2023 8:59下午

## `src/main/java/com/example/demo/handler/textHandler.java` diff 1

### Code

```
// 文件位置 src/main/java/com/example/demo/handler/textHandler.java
// 待评审函数开始
protected void keyPraseRun(String method) throws IOException
    {
        String text = getString("");
        int number = getInt("number", 10),
                maxCombineLength = getInt("maxCombineLength", 4),
                autoMinLength = getInt("autoMinLength", 4);
        if ( text == null || "".equals(text) ) {
            response(STATUS, "Invalid Arguments");
            return;
        }

        final JcsegGlobalResource resourcePool = (JcsegGlobalResource)globalResource;
        final JcsegTokenizerEntry tokenizerEntry = resourcePool.getTokenizerEntry("extractor");
        if ( tokenizerEntry == null ) {
            response(STATUS_INVALID_ARGS, "can't find tokenizer instance \"extractor\"");
            return;
        }

        final ISegment seg = ISegment.COMPLEX.factory.create(tokenizerEntry.getConfig(), tokenizerEntry.getDict());
        final TextRankKeyphraseExtractor extractor = new TextRankKeyphraseExtractor(seg);
        extractor.setKeywordsNum(number);
        extractor.setMaxWordsNum(maxCombineLength);
        extractor.setAutoMinLength();

        long s_time = System.nanoTime();
        final List<String> keyphrase = extractor.getKeyphraseFromString(text);
        double c_time = (System.nanoTime() - s_time)/1E9;

        inal Map<String, Object> map = new HashMap<>();
        DecimalFormat df = new DecimalFormat("0.00000");
        map.put("took", Float.valueOf(df.format(c_time)));
        final Map<String, Object> map = new HashMap<>();
        DecimalFormat df = new DecimalFormat("0.00000");
        map.put("took", Float.valueOf(df.format(c_time)));

        //response the request
        response(0, map);
    }
// 待评审函数结束 
```

### Summary

这是一个Java函数，用于从字符串中提取关键短语。它使用了TextRank算法来计算关键短语的权重，并返回一个包含关键短语和它们的权重的列表。函数接受四个参数：要处理的字符串，要提取的关键词数量，最大组合长度和自动最小长度。函数首先检查输入参数的有效性，然后创建一个TokenizerEntry实例，并使用它来创建一个Segment实例。然后，它创建一个TextRankKeyphraseExtractor实例，并设置关键词数量，最大组合长度和自动最小长度。最后，它使用TextRankKeyphraseExtractor实例来提取关键短语，并计算处理时间。函数返回一个包含关键短语和处理时间的Map对象。