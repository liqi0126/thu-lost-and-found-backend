import jieba
import numpy as np
import math

MATCHING_THRESHOLD = 0.8

NTC_LOC_WT = 2  # notice_location_weight
NTC_TIME_WT = 5  # notice_time_weight
NTC_DESC_WT = 10  # notice_description_weight
NTC_EXTRA_WT = 1  # notice_extra_weight

PROP_ATR_WT = 10  # property_attribute_weight
PROP_TAG_WT = 5  # property_tag_weight
PROP_DESC_WT = 10  # property_description_weight
PROP_EXTRA_WT = 1  # property_extra_weight


def sigmoid(x):
    return math.exp(-np.logaddexp(0, -x))


def word_matching_sim(words1, words2):
    if len(words1) == 0 or len(words2) == 0:
        return 0
    return 2 * len([1 for w1 in words1 if w1 in words2]) / (len(words1) + len(words2))


def json_matching_sim(json1, json2):
    if len(json1) == 0 or len(json2) == 0:
        return 0
    return 2 * len([1 for key in json1 if (key in json2 and json1[key] == json2[key])]) / (len(json1) + len(json2))


def matching(lost_notice, found_notice):
    base = 0
    match_degree = 0
    found_property = found_notice.property
    lost_property = lost_notice.property

    ###########################################
    # cannot matched cases
    ###########################################
    if lost_property.template_id != found_property.template_id:
        return -1

    if lost_notice.est_lost_start_datetime is not None and found_notice.found_datetime is not None:
        if lost_notice.est_lost_start_datetime > found_notice.found_datetime:
            return -1

    ###########################################
    # NOTICE
    ###########################################
    # places
    if lost_notice.lost_location == found_notice.found_location:
        match_degree += NTC_LOC_WT
        base += NTC_LOC_WT

    # time
    if lost_notice.est_lost_start_datetime is not None and found_notice.found_datetime is not None:
        base += NTC_TIME_WT
        if lost_notice.est_lost_start_datetime > found_notice.found_datetime:
            match_degree += 0
        elif (found_notice.found_datetime - lost_notice.est_lost_start_datetime).days <= 5:
            match_degree += NTC_TIME_WT
        else:
            match_degree += NTC_TIME_WT * (1 - 2 * sigmoid((found_notice.found_datetime - lost_notice.est_lost_start_datetime).days - 5) - 0.5)

    # notice description
    found_notice_desc = None
    if found_notice.description is not None:
        found_notice_desc = jieba.lcut(found_notice.description)

    lost_notice_desc = None
    if lost_notice.description is not None:
        lost_notice_desc = jieba.lcut(lost_notice.description)

    if found_notice_desc is not None and lost_notice_desc is not None:
        match_degree += NTC_DESC_WT * word_matching_sim(found_notice_desc, lost_notice_desc)
        base += NTC_DESC_WT

    # notice extra
    if lost_notice.extra is not None and found_notice.extra is not None:
        match_degree += NTC_EXTRA_WT * json_matching_sim(lost_notice.extra, found_notice.extra)
        base += NTC_EXTRA_WT

    ###########################################
    # PROPERTY
    ###########################################
    found_property = found_notice.property
    lost_property = lost_notice.property

    # property attributes
    match_degree += PROP_ATR_WT * json_matching_sim(found_property.attributes, lost_property.attributes)
    base += PROP_ATR_WT

    # property tags
    found_tags = [tag.name for tag in found_property.tags.all()]
    lost_tags = [tag.name for tag in lost_property.tags.all()]
    match_degree += PROP_TAG_WT * word_matching_sim(found_tags, lost_tags)
    base += PROP_TAG_WT

    # property description
    lost_property_desc = None
    if lost_property.description is not None:
        lost_property_desc = jieba.lcut(lost_property.description)

    found_property_desc = None
    if found_property.description is not None:
        found_property_desc = jieba.lcut(found_property.description)

    if lost_property_desc is not None and found_property_desc is not None:
        match_degree += PROP_DESC_WT * word_matching_sim(lost_property_desc, found_property_desc)
        base += PROP_DESC_WT

    # property extra
    if lost_property.extra is not None and found_property.extra is not None:
        match_degree += PROP_EXTRA_WT * json_matching_sim(lost_property.extra, found_property.extra)
        base += PROP_EXTRA_WT

    return match_degree / base

