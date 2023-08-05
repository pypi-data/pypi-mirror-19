# Installation
```
pip install DateTimeRange
```


# Usage
datetime.datetime instance can be used as an argument value as well as time-string in the below examples. 

## Create and convert to string
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
str(time_range)
```

    '2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900'

## Compare time range
```python
from datetimerange import DateTimeRange
lhs = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
rhs = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
print "lhs == rhs: ", lhs == rhs
print "lhs != rhs: ", lhs != rhs
```

    lhs == rhs:  True
    lhs != rhs:  False

## Move the time range
```python
import datetime
from datetimerange import DateTimeRange
value = DateTimeRange("2015-03-22T10:10:00+0900", "2015-03-22T10:20:00+0900")
print value + datetime.timedelta(seconds=10 * 60)
print value - datetime.timedelta(seconds=10 * 60)
```

    2015-03-22T10:20:00+0900 - 2015-03-22T10:30:00+0900
    2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900
    

## Change string conversion format
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
time_range.start_time_format = "%Y/%m/%d"
time_range.end_time_format = "%Y/%m/%dT%H:%M:%S%z"
time_range
```

    2015/03/22 - 2015/03/22T10:10:00+0900

## Add elapsed time when conversion to string
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
time_range.is_output_elapse = True
time_range
```

    2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)

## Change separator of the converted string
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
time_range.separator = " to "
time_range
```

    2015-03-22T10:00:00+0900 to 2015-03-22T10:10:00+0900

## Get start time as datetime.datetime
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
time_range.start_datetime
```

    datetime.datetime(2015, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))

## Get start time as string (formatted with `start_time_format`)
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
print time_range.get_start_time_str()
time_range.start_time_format = "%Y/%m/%d %H:%M:%S"
print time_range.get_start_time_str()
```

    2015-03-22T10:00:00+0900
    2015/03/22 10:00:00

## Get end time as datetime.datetime
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
time_range.end_datetime
```

    datetime.datetime(2015, 3, 22, 10, 10, tzinfo=tzoffset(None, 32400))

## Get end time as string (formatted with `end_time_format`)
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
print time_range.get_end_time_str()
time_range.end_time_format = "%Y/%m/%d %H:%M:%S"
print time_range.get_end_time_str()
```

    2015-03-22T10:10:00+0900
    2015/03/22 10:10:00
    
## Get datetime.timedelta (from start_datetime to the end_datetime)
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
time_range.timedelta
```

    datetime.timedelta(0, 600)

## Get timedelta as seconds (from start_datetime to the end_datetime)
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
time_range.get_timedelta_second()
```

    600.0

## Get iterator
```python
import datetime
from datetimerange import DateTimeRange

time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2015-01-04T00:00:00+0900")
for value in time_range.range(datetime.timedelta(days=1)):
    print value
```

    2015-01-01 00:00:00+09:00
    2015-01-02 00:00:00+09:00
    2015-01-03 00:00:00+09:00
    2015-01-04 00:00:00+09:00

```python
from datetimerange import DateTimeRange
from dateutil.relativedelta import relativedelta

time_range = DateTimeRange("2015-01-01T00:00:00+0900", "2016-01-01T00:00:00+0900")
for value in time_range.range(relativedelta(months=+4)):
    print value
```

    2015-01-01 00:00:00+09:00
    2015-05-01 00:00:00+09:00
    2015-09-01 00:00:00+09:00
    2016-01-01 00:00:00+09:00

## Set start time
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange()
print time_range
time_range.set_start_datetime("2015-03-22T10:00:00+0900")
print time_range
```

    NaT - NaT
    2015-03-22T10:00:00+0900 - NaT
    
## Set end time
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange()
print time_range
time_range.set_end_datetime("2015-03-22T10:10:00+0900")
print time_range
```

    NaT - NaT
    NaT - 2015-03-22T10:10:00+0900
    
## Set time range (set both start and end time)
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange()
print time_range
time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
print time_range
```

    NaT - NaT
    2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900
    
## Test whether the time range is set
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange()
print time_range.is_set()
time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
print time_range.is_set()
```

    False
    True

## Validate time inversion
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:10:00+0900", "2015-03-22T10:00:00+0900")
try:
    time_range.validate_time_inversion()
except ValueError:
    print "time inversion"
```

    time inversion
    
## Test whether the time range is valid
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange()
print time_range.is_valid_timerange()
time_range.set_time_range("2015-03-22T10:20:00+0900", "2015-03-22T10:10:00+0900")
print time_range.is_valid_timerange()
time_range.set_time_range("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
print time_range.is_valid_timerange()
```

    False
    False
    True
    
## Test whether a value within the time range
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
print "2015-03-22T10:05:00+0900" in time_range
print "2015-03-22T10:15:00+0900" in time_range

time_range_smaller = DateTimeRange("2015-03-22T10:03:00+0900", "2015-03-22T10:07:00+0900")
print time_range_smaller in time_range
```

    True
    False
    True
    
## Test whether a value intersect the time range
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
time_range.is_intersection(x)
```

    True

## Make an intersected time range
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
time_range.intersection(x)
time_range
```

    2015-03-22T10:05:00+0900 - 2015-03-22T10:10:00+0900

## Make an encompassed time range
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
x = DateTimeRange("2015-03-22T10:05:00+0900", "2015-03-22T10:15:00+0900")
time_range.encompass(x)
time_range
```

    2015-03-22T10:00:00+0900 - 2015-03-22T10:15:00+0900

## Truncate time range
```python
from datetimerange import DateTimeRange
time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
time_range.is_output_elapse = True
print "before truncate: ", time_range
time_range.truncate(10)
print "after truncate:  ", time_range
```

    before truncate:  2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900 (0:10:00)
    after truncate:   2015-03-22T10:00:30+0900 - 2015-03-22T10:09:30+0900 (0:09:00)


# Documentation
http://datetimerange.readthedocs.org/en/latest/datetimerange.html


## Note
Use not the daylight saving time (DST) offset, but the standard time offset
when you use datetime string as an argument.
DateTimeRange class will automatically calculate daylight saving time.
Some examples are below

```console
>>>from datetimerange import DateTimeRange
>>>time_range = DateTimeRange("2015-03-08T00:00:00-0400", "2015-03-08T12:00:00-0400")
>>>time_range.timedelta
datetime.timedelta(0, 39600)  # 11 hours
```

```console
>>>from datetimerange import DateTimeRange
>>>time_range = DateTimeRange("2015-11-01T00:00:00-0400", "2015-11-01T12:00:00-0400")
>>>time_range.timedelta
datetime.timedelta(0, 46800)  # 13 hours
```


# Dependencies
Python 2.5+ or 3.3+

- [python-dateutil](https://pypi.python.org/pypi/python-dateutil/)
- [pytz](https://pypi.python.org/pypi/pytz)

## Test dependencies

-   [pytest](https://pypi.python.org/pypi/pytest)
-   [pytest-runner](https://pypi.python.org/pypi/pytest-runner)
-   [tox](https://pypi.python.org/pypi/tox)

