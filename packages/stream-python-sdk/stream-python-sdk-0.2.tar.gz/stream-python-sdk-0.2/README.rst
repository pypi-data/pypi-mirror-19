Stream Python SDK
==============

Stream Python SDK实现了Stream 日志操作接口，基于此SDK能方便快速地实现Python应用程序来对订阅日志进行相关操作。

支持的功能
----------

日志操作接口
^^^^^^^^^^^^

* Get Subscription Position —— 获取订阅日志位置
* Get Logs —— 获取指定订阅日志

接口实现
--------

在调用对象操作接口前需要生成一个stream_client.StreamClient类的实例。且在调用操作接口时，都有可能抛出异常，可以使用'stream.exceptions.ServiceException'捕获stream服务器异常错误，使用'stream.exceptions.ClientException'捕获stream客户端异常错误。

stream_client.StreamClient对象实例化

使用举例

::

    client = stream_client.StreamClient(
        access_key_id="string",
        access_key_secret="string"
    )

参数说明

* access_key_id(string) -- 访问凭证ID。
* access_key_secret(string) -- 访问凭证密钥。

stream_client.StreamClient可能引发的所有异常类型

在程序运行过程中，如果遇到错误，Python SDK会抛出相应的异常。所有异常均属于StreamException类，其下分为两个子类：ClientException、ServiceException。在调用Python SDK接口的时候，捕捉这些异常并打印必要的信息有利于定位问题。

ClientException
:::::::::::::::

ClientException包含SDK客户端的异常。比如，上传对象时对象名为空，就会抛出该异常。
ClientException类下有如下子类，用于细分客户端异常：

.. list-table::
    :widths: 5 10
    :header-rows: 1

    * - 类名
      - 抛出异常的原因
    * - InvalidParameter
      - 传入的参数非法
    * - SerializationError
      - 上传对象序列化失败
    * - ConnectionError
      - 连接服务端异常
    * - ConnectionTimeout
      - 连接服务端超时

ServiceException
::::::::::::::::

ServiceException包含Stream服务器返回的异常。当Stream服务器返回4xx或5xx的HTTP错误码时，Python SDK会将Stream Server的响应转换为ServiceException。
ServiceException类下有如下子类，用于细分Stream服务器返回的异常：

.. list-table::
    :widths: 5 10
    :header-rows: 1

    * - 类名
      - 抛出异常的原因
    * - BadRequestError
      - 服务端返回HTTP 400响应
    * - ForbiddenError
      - 服务端返回HTTP 403响应
    * - NotFoundError
      - 服务端返回HTTP 404响应
    * - MethodNotAllowedError
      - 服务端返回HTTP 405响应
    * - ConflictError
      - 服务端返回HTTP 409响应
    * - LengthRequiredError
      - 服务端返回HTTP 411响应
    * - RequestedRangeNotSatisfiableError
      - 服务端返回HTTP 416响应
    * - InternalServerErrorError
      - 服务端返回HTTP 500响应
    * - NotImplementedError
      - 服务端返回HTTP 501响应
    * - ServiceUnavailableError
      - 服务端返回HTTP 503响应

stream_client.StreamClient的使用和异常处理的示例代码

::

 try:
    resp = stream_client.StreamClient.XXX(
        subscription_name=subscription_name,
        position_type=position_type
    )
 except stream.exceptions.ServiceException as e:
    print (
        'ServiceException: %s\n'
        'message: %s\n'
    ) % (
        e,
        e.message       # 错误描述信息
    )
 except stream.exceptions.ClientException as e:
    print (
        'ClientException: %s\n'
        'message: %s\n'
    ) % (
        e,
        e.message       # 客户端错误信息
    )

日志操作接口
^^^^^^^^^^^^

Get Subscription Position
:::::::::::::

使用举例

::

    resp = client.get_subscription_position(
        subscription_name=topic_name,
        position_type=position_type
    )

参数说明

* subscription_name(string) -- 订阅主题名称。
* position_type(string) -- 获取位置类型。

返回值举例

::

    {
        "position": "dGVzdDIw33YxMjE1MTkwMy5kZWZhdWx0LXdtM3pxOjEw"
    }

返回值说明
返回值为字典类型

* position(string) -- 日志位置。


Get Logs
:::::::::::::::::::::::

使用举例

::

    resp = client.get_logs(
        subscription_name=topic_name,
        logs_position=logs_position,
        limit=limit
    )

参数说明

* subscription_name(string) -- 订阅主题名称。
* logs_position(string) -- 日志位置。
* limit(int) -- 获取日志条数限制。

返回值举例

::

    {
        "subscription_logs": [
            {
                "timestamp": 1482467113427,
                "message": "ksjfkajfkasfs"
            }
        ],
        "count": 1,
        "next_position": "dGVzdDIwMTYxMjE1MTkwMy5kZWZhdWx0LXdtM3pxOjEx",
        "reached_ending": false
    }