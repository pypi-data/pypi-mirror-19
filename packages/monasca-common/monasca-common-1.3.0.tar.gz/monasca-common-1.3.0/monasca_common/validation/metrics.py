# (C) Copyright 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import ujson

# This is used to ensure that metrics with a timestamp older than
# RECENT_POINT_THRESHOLD_DEFAULT seconds (or the value passed in to
# the MetricsAggregator constructor) get discarded rather than being
# input into the incorrect bucket. Currently, the MetricsAggregator
# does not support submitting values for the past, and all values get
# submitted for the timestamp passed into the flush() function.
RECENT_POINT_THRESHOLD_DEFAULT = 3600
VALUE_META_MAX_NUMBER = 16
VALUE_META_VALUE_MAX_LENGTH = 2048
VALUE_META_NAME_MAX_LENGTH = 255

INVALID_CHARS = "<>={}(),\"\\\\;&"
RESTRICTED_DIMENSION_CHARS = re.compile('[' + INVALID_CHARS + ']')
RESTRICTED_NAME_CHARS = re.compile('[' + INVALID_CHARS + ' ' + ']')


class InvalidMetricName(Exception):
    pass


class InvalidDimensionKey(Exception):
    pass


class InvalidDimensionValue(Exception):
    pass


class InvalidValue(Exception):
    pass


class InvalidValueMeta(Exception):
    pass


class InvalidTimeStamp(Exception):
    pass


def validate(metrics):
    if isinstance(metrics, list):
        for metric in metrics:
            validate_metric(metric)
    else:
        validate_metric(metrics)


def validate_metric(metric):
    validate_name(metric['name'])
    validate_value(metric['value'])
    validate_timestamp(metric['timestamp'])
    if "dimensions" in metric:
        validate_dimensions(metric['dimensions'])
    if "value_meta" in metric:
        validate_value_meta(metric['value_meta'])


def validate_value_meta(value_meta):
    if len(value_meta) > VALUE_META_MAX_NUMBER:
        msg = "Too many valueMeta entries {0}, limit is {1}: valueMeta {2}".\
            format(len(value_meta), VALUE_META_MAX_NUMBER, value_meta)
        raise InvalidValueMeta(msg)
    for key, value in value_meta.iteritems():
        if not key:
            raise InvalidValueMeta("valueMeta name cannot be empty: key={}, "
                                   "value={}".format(key, value))
        if len(key) > VALUE_META_NAME_MAX_LENGTH:
            msg = "valueMeta name too long: {0} must be {1} characters or " \
                  "less".format(key, VALUE_META_NAME_MAX_LENGTH)
            raise InvalidValueMeta(msg)

    try:
        value_meta_json = ujson.dumps(value_meta)
        if len(value_meta_json) > VALUE_META_VALUE_MAX_LENGTH:
            msg = "valueMeta name value combinations must be {0} characters " \
                  "or less: valueMeta {1}".format(VALUE_META_VALUE_MAX_LENGTH,
                                                  value_meta)
            raise InvalidValueMeta(msg)
    except Exception:
        raise InvalidValueMeta("Unable to serialize valueMeta into JSON")


def validate_dimensions(dimensions):
    for k, v in dimensions.iteritems():
        if not isinstance(k, (str, unicode)):
            msg = "invalid dimension key type: " \
                  "{0} in {1} is not a string type".format(k, dimensions)
            raise InvalidDimensionKey(msg)
        if len(k) > 255 or len(k) < 1:
            msg = "invalid length for dimension key {0}: {1}".\
                format(k, dimensions)
            raise InvalidDimensionKey(msg)
        if RESTRICTED_DIMENSION_CHARS.search(k) or re.match('^_', k):
            msg = "invalid characters in dimension key {0}: {1}".\
                format(k, dimensions)
            raise InvalidDimensionKey(msg)

        if not isinstance(v, (str, unicode)):
            msg = "invalid dimension value type: {0} for key {1} must be a " \
                  "string: {2}".format(v, k, dimensions)
            raise InvalidDimensionValue(msg)
        if len(v) > 255 or len(v) < 1:
            msg = "invalid length for dimension value {0} in key {1}: {2}".\
                format(v, k, dimensions)
            raise InvalidDimensionValue(msg)
        if RESTRICTED_DIMENSION_CHARS.search(v):
            msg = "invalid characters in dimension value {0} for key {1}: " \
                  "{2}".format(v, k, dimensions)
            raise InvalidDimensionValue(msg)


def validate_name(name):
    if not isinstance(name, (str, unicode)):
        msg = "invalid metric name type: {0} is not a string type ".format(
            name)
        raise InvalidMetricName(msg)
    if len(name) > 255 or len(name) < 1:
        msg = "invalid length for metric name: {0}".format(name)
        raise InvalidMetricName(msg)
    if RESTRICTED_NAME_CHARS.search(name):
        msg = "invalid characters in metric name: {0}".format(name)
        raise InvalidMetricName(msg)


def validate_value(value):
    if not isinstance(value, (int, long, float)):
        msg = "invalid value type: {0} is not a number type for metric".\
            format(value)
        raise InvalidValue(msg)


def validate_timestamp(timestamp):
    if not isinstance(timestamp, (int, float)):
        msg = "invalid timestamp type: {0} is not a number type for " \
              "metric".format(timestamp)
        raise InvalidTimeStamp(msg)
