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
