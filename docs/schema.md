This defines the schema layout for various log formats.
Each log format has its own schema guide for how the log entries should be structured
and which fields are required.

# JSON Schema Layout

**Timestamp Field**:
   - Format: String or Datetime object
   - Purpose: Indicates the exact timestamp of the log event.
   - Examples: 
   - "2020-02-01T12:34:56Z"
   - "2020-02-01 12:34:56"
   - Common Field Name(s): "@timestamp", "timestamp"

**Log Level**:
   - Format: String (uppercased)
   - Purpose: Represents the severity of the log message.
   - Examples:
   - "DEBUG", "INFO", "ERROR", "CRITICAL", "TRACE", "WARN"
   - Common Field Name(s): "log.level", "level", "severity"

**Source**:
   - Format: String
   - Purpose: Identifies the source from which the log originates (e.g., host, service name).
   - Examples:
   - "localhost", "serviceA", "app1"
   - Common Field Name(s): "source", "host", "service.name"

**Module/Logger**:
   - Format: String
   - Purpose: The name of the component or module that generated the log message.
   - Examples:
   - "app.main", "com.example.MyClass", "my_module"
   - Common Field Name(s): "log.logger", "module", "loggerName"

**Message**:
   - Format: String
   - Purpose: The main content or message of the log.
   - Examples:
   - "Error processing file", "Service started", "User login successful"
   - Common Field Name(s): "message", "msg"

**Additional Fields**:
   - Format: Various (String, Integer, etc.)
   - Purpose: Extra data associated with the log event.


Example Layout(s)
----------------
**JSON Schema (for Syslog format)**
```json
{
   "timestamp": "2003-10-11T22:14:15.000003+04:00",
   "level": "CRITICAL",
   "source": "192.18.0.9",
   "module": "su",
   "message": "'su root' failed for lonvick on /dev/pts/8",
   "additional_fields": {
      "eventSource": "Application",
      "eventID": "1011"
   }
}
```
**JSON Schema (for Log4j format)**
```json
{
   "timestamp": "2020-02-01T12:34:56.000+0000",
   "level": "ERROR",
   "loggerName": "com.example.MyClass",
   "message": "An error occurred while processing the data.",
   "threadName": "main",
   "mdc": {
      "userId": "12345",
      "sessionId": "abc123"
   },
   "exception": "java.lang.NullPointerException at ...",
   "loggerContext": "app.logging"
}
```
**JSON Schema (for ECS format)**
```json
{
   "@timestamp": "2020-02-01T12:34:56.000+0000",
   "log.level": "ERROR",
   "log.logger": "com.example.MyClass",
   "message": "An error occurred while processing the data.",
   "event.category": "error",
   "event.action": "process_failed",
   "ecs.version": "1.6.0",
   "host.name": "server01",
   "user.name": "john_doe",
   "service.name": "my_service"
}
```

Notes
------
- The **timestamp** field is not required but encourage.
- The **level** field indicates the severity of the log message and is not required but encourage.
- The **message** field is always required, as it provides the context of the log.
- The **source** and **module/logger** fields help trace the origin of the log message and is not required but encourage.
- Additional fields are optional but can provide more context, especially in systems requiring traceability or correlation.
- For each log format (e.g., Syslog, Log4j, JSON), the exact names and structure of these fields may vary.
- Refer to the corresponding log format schema for more details on specific field names.

# Log4j (NO-JSON) Schema Layout

Log4j follows a specific layout schema, commonly referred to as the **Log4j Default Layout**.

Default Log4j format (as per Log4j 2.x) contains the following values

**timestamp**:
   - Format: ISO 8601 formatted string (e.g., `2020-02-01T12:34:56.000+0000`)
   - Represents the exact time when the log entry was created.
   - Example: `2020-02-01T12:34:56.000+0000`

**level**:
   - Format: String (uppercased)
   - Describes the severity level of the log message.
   - Example: `ERROR`

**logger** (Module/Logger):
   - Format: String
   - Identifies the logger that generated the log entry, usually the class or module name.
   - Example: `com.example.MyClass`

**message**:
   - Format: String
   - The actual log message.
   - Example: `An error occurred while processing the data.`

**thread**:
   - Format: String
   - The name of the thread that generated the log entry.
   - Example: `[main]`

Example Layout
----------------
```
2020-09-10 [api-thread] DEBUG api.controller - Creating new user
```

Notes
-----------------
- The **timestamp** field is not required but encourage.
- The **level** field indicates the severity of the log message and is not required but encourage.
- The **message** field is always required, as it provides the context of the log.
- The **source** and **module/logger** fields help trace the origin of the log message and is not required but encourage.
- Additional fields are optional but can provide more context, especially in systems requiring traceability or correlation.
- For each log format (e.g., Syslog, Log4j, JSON), the exact names and structure of these fields may vary.
- Refer to the corresponding log format schema for more details on specific field names.

# Syslog Format Layout:

The Syslog format follows the **Syslog Protocol** (RFC 5424) and (RFC 3164) and can include **Syslog header** information and **message content**.

Default Syslog format typically contains the following fields:

**timestamp**:
   - Format: ISO 8601 formatted string or "Syslog date".
   - Represents the exact time when the log entry was generated.
   - Example: `2020-02-01T12:34:56.000+0000` or `Jan 10 14:33:15`

**level**:
   - Format: Integer (Syslog severity level, 0-7), or string equivalent (e.g., "DEBUG", "INFO", "ERROR").
   - Describes the severity of the log message.
   - Example: `INFO`

**source**:
   - Format: String (usually the host or device that generated the log).
   - Example: `192.18.0.9`

**message**:
   - Format: String
   - The actual log message content.
   - Example: `"message": "'su root' failed for lonvick on /dev/pts/8"`

**facility**:
   - Format: Integer (Syslog facility code)
   - Identifies the subsystem or application generating the log.
   - Example: `auth`

**hostname**:
   - Format: String
   - The name of the host or machine generating the log entry.
   - Example: `localhost`

**program**:
   - Format: String
   - The name of the program or service generating the log.
   - Example: `su`

Example Layout
-----------------------------
**RFC 3164**
```
<165>Jun 1 08:55:00 notaserver testapp: Unexpected error occurred
```
**RFC 5424**
```
<34>1 2021-01-01T00:00:00+00:00 192.168.0.100 systemd 12 ID123 [sdid@12345 eventSource='system' eventID='1001'][login] User 'root' logged in
```

Notes
-----------------
- **timestamp** field is essential to identify when the log was created.
- **level** field is usually a severity level, represented by integers 0-7, but may also be string values (e.g., "INFO").
- **message** is the most important field in Syslog, providing details of the log entry.
- Syslog may also include **facility**, **hostname**, and **program** for better traceability of the log's origin.
- Depending on the Syslog version (e.g., RFC 5424), additional fields might be present.
- **priority** header is converted to respective severity levels

# XML Layout

> XML logs must start with a xml declaration tag: `<?xml version="1.0" encoding="UTF-8" standalone="no"?>`
## Java Util Logging (JLU)

The Java Util Logging (JUL) XML format follows a structured Document Type Definition (DTD) that defines the elements and structure of a log message. Below is the **DTD** specification:

### Root Element
- **`log`**: The root element that contains multiple `record` entries.

### Log Record Structure
Each log entry is represented by a `record` element containing the following fields:

#### **Timestamp Fields**
- **`date`**: The date and time when the log record was created (ISO 8601 format).
- **`millis`**: Time in milliseconds since January 1, 1970 (UTC).
- **`nanos`** *(optional)*: Nanosecond precision timestamp (added in JDK 9).

#### **Identification Fields**
- **`sequence`**: A unique sequence number within the JVM instance.
- **`thread`**: Integer representing the thread ID that generated the log.

#### **Source Information**
- **`logger`** *(optional)*: The logger's name that created the log entry.
- **`class`** *(optional)*: Fully qualified class name that issued the logging call.
- **`method`** *(optional)*: Method name that issued the log (may include argument types).

#### **Severity Level**
- **`level`**: The severity level (e.g., `"SEVERE"`, `"INFO"`, `"WARNING"`, or an integer equivalent).

#### **Message and Localization**
- **`message`**: The actual log message content.
- **`key`** *(optional)*: If localized, the original message key.
- **`catalog`** *(optional)*: Resource bundle name used for localization.
- **`param`** *(optional, multiple)*: String values of the log parameters.

#### **Exception Handling**
- **`exception`** *(optional)*: Captures exception details if an error occurred.
  - **`message`** *(optional)*: Exception message.
  - **`frame`** *(multiple)*: Represents stack trace frames.
    - **`class`**: Class where the exception occurred.
    - **`method`**: Method where the exception occurred.
    - **`line`** *(optional)*: Line number in the source file.

Example
----------------
```xml
<log>
  <record>
    <date>2025-03-08T14:30:00Z</date>
    <millis>1709892600000</millis>
    <sequence>12345</sequence>
    <logger>com.example.MyApp</logger>
    <level>INFO</level>
    <class>com.example.MyClass</class>
    <method>myMethod</method>
    <thread>10</thread>
    <message>Hello, this is a log message!</message>
  </record>
</log>
```

## Windows Events
See http://schemas.microsoft.com/win/2004/08/events/event for schema details
or Microsoft Learn

# SIP Common Log Format (SIP-CLF)

- **Timestamp** — Date and time of the request or re-
sponse represented as the number of seconds and
milliseconds since the Unix epoch.
- **Size of the SIP CLF record** — The total number of
bytes that comprise the SIP CLF record. This allows
systems that do post-analysis on the log ﬁle to skip
the record if it is not of interest.
- **Message type** — An indicator of whether the SIP
message is a request or a response. The allowable
values for this ﬁeld are R (for Request) and r (for
response).
- **Directionality** - An indicator of whether the SIP
message is received by the SIP entity or sent by the
SIP entity. The allowable values for this ﬁeld are s
(for message sent) and r (for message received).
- **Source:port:xport** — The DNS name or IP address
of the upstream client, including the port number
and the transport over which the SIP message was
received. The port number must be separated from
the DNS name or IP address by a single `:`. The
transport must be separated from the port by a sin-
gle `:`. The allowable values for the transport are
`tcp`, `tls`, `sctp`, and `udp`
- **Destination:port:xport** — The DNS name or IP ad-
dress of the downstream server, including the port
number. The port number must be separated from
the DNS name or IP address by a single `:`. The
transport must be separated from the port by a sin-
gle `:`. The allowable values for the transport are
`tcp`, `tls`, `sctp`, and `udp`
- **From** — The From URI, including the tag. In SIP,
the From URI speciﬁes the sender of a request. The
tag is a URI parameter that is used to identify a dia-
log between two endpoints.
o — The To URI, including the tag. In SIP, the To
URI is the logical recipient of the request. The tag
has the same semantics as that of the From URI.
- **Callid** — The Call-ID header. In SIP, a Call-ID
header groups all transactions exchanged between
a UAC and UAS.
- **CSeq** — The CSeq header, used for sequencing.
- **R-URI** — The Request-URI, including any URI
parameters. In SIP, the R-URI identifies the ulti-
mate recipient of the request. SIP intermediaries
use it to route the request towards the destination
UAS. The R-URI occurs on the topmost line of a
SIP request (it is not present in a SIP response)
- **Status** — The SIP response status code (i.e., 100,
200, etc.) Status lines occur only in responses
- **Server-Txn** - Server transaction identification code - the transaction identifier associated with the server
transaction. Implementations can reuse the UAS
server transaction identifier (the topmost branch-id
of the incoming request, with or without the magic
cookie), or they could generate a unique identifi-
cation string for a server transaction (this identifier
needs to be locally unique to the server only.) This
identifier is used to correlate ACKs and CANCELs
to an INVITE transaction; it is also used to aid in
forking.
- **Client-Txn** - Client transaction identification code -
this field is used to associate client transactions with
a server transaction for forking proxies or B2BUAs.
Upon forking, implementations can reuse the value
they inserted into the topmost Via header’s branch
parameter, or they can generate a unique identifica-
tion string for the client transaction.

**Template Format Layout**

Record-size Timestamp Message-type Directionality CSeq R-URI Destination:port:xport Source:port:xport To From Call-ID Status Server-Txn Client-Txn [TLV [TLV]...]

Example
----------------
```
170 1275930748.991 r r INVITE-43 - 203.0.113.200:5060:udp [2001:db8::9]:5060:udp sip:bob@example.net;b2-2
sip:alice@example.com;tag=a1-1 tr-88h@example.com 487 s-1-tr c-2-tr
```

# NCSA Common Log Format

The NCSA Common Log Format (CLF) is a standardized text-based logging format used by web servers and various applications to log requests. It provides a consistent way to track access logs and analyze web traffic.

## Types of Common Log Formats

There are three main types of CLF:

###  Common Log Format (CLF)

The Common Log Format is the simplest version, containing essential request details such as the client IP, timestamp, request line, response status, and bytes sent.

- **host**: The IP address or hostname of the client.
- **ident**: Identity of the user (typically -, as this is rarely used).
- **authuser**: Authenticated username (if applicable, otherwise -).
- **date**: Timestamp of the request in [dd/Mon/yyyy:hh:mm:ss z] format.
- **request**: The HTTP request method, URL, and protocol.
- **status**: HTTP response status code (e.g., 200, 404).
- **bytes**	Size of the response body in bytes (- if unknown).

**Template Format**

host ident authuser [date] "request" status bytes

#### Example
----------------
```
192.168.1.1 - - [10/Mar/2025:14:22:35 +0000] "GET /index.html HTTP/1.1" 200 1024
```
### Combined Log Format (CLF - Combined)

The Combined Log Format extends the Common Log Format by adding Referer and User-Agent fields, making it useful for tracking user behavior.

- **referrer:** The URL which linked the user to your site. (Optional)
- **user_agent:** The Web browser and platform used by the visitor to your site.(Optional)
- **cookies:** Cookies are pieces of information that the HTTP server can send back to client along the with the requested resources. A client's browser may store this information and subsequently send it back to the HTTP server upon making additional resource requests. The HTTP server can establish multiple cookies per HTTP request.

**Template Format**

host ident authuser [date] "request" status bytes "referer" "user-agent" "cookies"

#### Example
----------------
```
125.125.125.125 - dsmith [10/Oct/1999:21:15:05 +0500] "GET /index.html HTTP/1.0" 200 1043 "http://www.ibm.com/" "Mozilla/4.05 [en] (WinNT; I)" "USERID=CustomerA;IMPID=01234"
```

# Common Event Format

- **CEF:Version**: A mandatory header indicating the CEF version (e.g., CEF:0).
- **Device Vendor**: The vendor of the device generating the event.
- **Device Product**: The specific product or device type.
- **Device Version**: The version of the device product.
- **Signature ID**: A unique identifier for the security event or rule that triggered the event.
- **Name**: A descriptive name for the event.
- **Severity**: A numeric value indicating the severity of the event (e.g., 1-10).
- **Extension**: A placeholder for additional fields, logged as key-value pairs (e.g., src=10.52.116.160 suser=admin).

**Template Format**

CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension

Example
----------------
```
CEF:0|Trend Micro|Deep Security Manager|<DSM version>|600|User Signed In|3|src=10.52.116.160 suser=admin target=admin msg=User signed in from 2001:db8::5
```
