---
url: /blog/linux/rkN88LE58RG
title: "Apache Struts2 S2-052 的远程执行代码漏洞发掘过程及解决办法"
date: 2018-05-14T04:45:01+08:00
description:
categories:
  - Linux
tags:
  - Linux
menu: main
---

> Apache（CVE-2017-9805）的远程执行代码漏洞

在这篇文章中，我将介绍我是如何定制标准LGTM查询找到一个远程执行代码漏洞Apache

Stru…

## Apache（CVE-2017-9805）的远程执行代码漏洞

在这篇文章中，我将介绍我是如何定制标准LGTM查询找到一个远程执行代码漏洞Apache

Struts的。有关此漏洞的更普遍的公告可以在这里找到。它已被定为CVE-2017-9805，一个安全公告可以在这里找到了Struts网站上，和Apache的Struts的解决了此漏洞的2.5.13版本的详细信息，可浏览这里。由于此漏洞的严重性质，详细信息（包括工作漏洞）已经从这篇文章省略。

我们强烈建议的Struts的用户升级到最新版本，以减轻这种安全风险。

我发现了这个漏洞是在Java中不安全的反序列化的结果。多个类似的漏洞已经大白于天下，近年来，经过克里斯·弗罗霍夫和加布里埃尔·劳伦斯发现在阿帕奇百科全书集合反序列化的缺陷，可导致任意代码执行。许多Java应用程序，至今已受这些漏洞。如果您想了解更多关于这种类型的漏洞，在关于这一主题LGTM文档页面是一个良好的开端。

## 检测Struts的不安全反序列化问题

LGTM使用写在一个专门设计的语言查询代码警报：QL。Java的许多查询的检测用户控制数据的潜在不安全反序列化。查询能够识别出其中数据被反序列化为Java对象的情况。这包括来自一个HTTP请求或从任何其他来源的连接数据。

此查询通过用户控制数据流到反序列化方法常见的方式。然而，一些项目使用略有不同的方法来接收远程用户输入。例如，Apache的Struts的使用ContentTypeHandler接口。这将数据转换为Java对象。由于这个接口的实现通常反序列化传递给它们的数据，每一个实现该接口的类是潜在的利益。用于检测用户控制数据的不安全反序列化标准QL查询可以很容易地适于识别用于处理用户输入此附加的方法。这是通过定义一个自定义的数据进行源。

在这种情况下，我们感兴趣的是从流动的数据toObject的方法，这是在所定义的ContentTypeHandler接口：

```
void toObject(Reader in, Object target);

```

其中包含的第一个参数的数据in传递到toObject应被视为被感染的：它是一个远程用户的控制之下，并且不应该被信任。我们想找个地方这种被污染的数据（源）流入反序列化方法（水槽），而不输入验证或消毒。

在QL DataFlow库通过在源代码中的各种步骤的跟踪被污染数据提供的功能。这就是所谓的污点跟踪。例如，数据被通过各种方法调用跟踪：

```
IOUtils.copy(remoteUserInput, output);   // output is now also tainted because the function copy preserves the data.

```

为了利用在污点跟踪功能DataFlow库，让我们定义的in参数ContentTypeHandler.toObject(…)作为污点源。首先，我们定义查询应如何认识的ContentTypeHandler接口和方法toObject。

```
/** The ContentTypeHandler Java class in Struts **/
class ContentTypeHandler extends Interface {
  ContentTypeHandler() {
    this.hasQualifiedName("org.apache.struts2.rest.handler", "ContentTypeHandler")
  }
}

/** The method `toObject` */
class ToObjectDeserializer extends Method {
  ToObjectDeserializer() {
    this.getDeclaringType().getASupertype*() instanceof ContentTypeHandler and
    this.getSignature = "toObject(java.io.Reader,java.lang.Object)"
  }
}

```

这里我们使用getASupertype\*()的匹配限制到具有任何类ContentTypeHandler的超类型。

下一步，我们要标记的的第一个参数toObject的方法不受信任的数据源，根据它的代码路径跟踪该数据。要做到这一点，我们扩展了FlowSource在QL的数据流库类：

```
/** Mark the first argument of `toObject` as a dataflow source **/
class ContentTypeHandlerInput extends FlowSource {
  ContentTypeHandlerInput() {
    exists(ToObjectDeserializer des |
      des.getParameter(0).getAnAccess() = this
    )
  }
}

```

直观上，这定义说到的第一个参数的任何接入toObject方法，如通过捕获ToObjectDeserializer以上，是流源。请注意，由于技术原因，流量来源必须是表达式。因此，我们确定所有访问该参数（这是表达式）作为光源，而不是参数本身（这是不是）。

现在，我们有一个数据流源的定义，我们可以看一下这个地方被污染数据是在不安全的反序列化方法使用的地方。我们没有定义方法（水槽）自己为它已经在用户控制数据查询的反序列化（第64行：UnsafeDeserializationSink我们需要将其定义复制到查询控制台）。利用这一点，我们的最终查询变为：

```
from ContentTypeHandlerInput source, UnsafeDeserializationSink sink
where source.flowsTo(sink)
select source, sink

```

这里我们使用的.flowsTo谓词FlowSource的跟踪，这样我们只当在执行反序列化不安全鉴定案件ContentTypeHandlerInput来源。

当我跑Struts的自定义查询后，得到一个结果。我验证了这个问题，它报告给Struts安全团队之前是一个真正的远程执行代码漏洞。他们已经在工作了一个解决方案，即使它是一个需要API的变化相当不平凡的任务非常快，反应灵敏。由于这一发现的严重性，我不会透露在这个阶段更多的细节。相反，我会更新在几个星期的时间这个博客帖子有更多的信息。

## 厂商的回复

- 2017年7月17日：首次披露。
- 2017年8月2日：API发生变化。
- 2017年8月14日：Struts补丁的审查。
- 2017年8月16日：漏洞正式认定为CVE-2017-9805
- 2017年9月5日：Struts的版本2.5.13发布

## 缓解不安全反序列化风险

LGTM运行标准用户控制数据的反序列化查询的所有Java项目。如果你的项目使用通过查询发现反序列化框架，并具有用户控制数据达到反序列化方法，您可能会看到该查询在LGTM相关警报。仔细检查任何结果。您还可以启用LGTM的拉力要求整合，以防止被合并到在首位的代码库这样的严重的安全问题。

如果你的项目使用其他反序列化框架，那么你就可以使用查询控制台创建标准查询自己的定制版本

## 影响版本

Struts 2.5 - Struts 2.5.12

## 规避方案

立即升级到Struts 2.5.13。注意： 新版本使用的默认限制策略会导致REST的一些函数停止工作，会对一些业务造成影响，建议使用以下新的接口：

```
§org.apache.struts2.rest.handler.AllowedClasses
§org.apache.struts2.rest.handler.AllowedClassNames
§org.apache.struts2.rest.handler.XStreamPermissionProvider

```

## 临时修复方案

1.停止使用REST插件。 2.限制服务端扩展类型:

```
<constant name="struts.action.extension" value="xhtmljson" />

```