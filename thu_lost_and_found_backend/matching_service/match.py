import jieba
import numpy as np
import math
import logging

from .models import MatchingHyperParam


def sigmoid(x):
    return math.exp(-np.logaddexp(0, -x))


def word_matching_num(words1, words2):
    if len(words1) == 0 or len(words2) == 0:
        return 0
    return len([1 for w1 in words1 if w1 in words2])
    # return 2 * len([1 for w1 in words1 if w1 in words2]) / (len(words1) + len(words2))


def json_matching_num(json1, json2):
    if len(json1) == 0 or len(json2) == 0:
        return 0
    return len([1 for key in json1 if (key in json2 and json1[key] == json2[key])])
    # return 2 * len([1 for key in json1 if (key in json2 and json1[key] == json2[key])]) / (len(json1) + len(json2))


def matching(lost_notice, found_notice):
    base = 0
    match_degree = 0
    found_property = found_notice.property
    lost_property = lost_notice.property

    matching_hyper = MatchingHyperParam.get_hyper()

    ###########################################
    # cannot matched cases
    ###########################################
    if lost_property.template_id != found_property.template_id:
        return 0

    ###########################################
    # NOTICE
    ###########################################
    # places
    if lost_notice.lost_location is not None and found_notice.found_location is not None:
        base += matching_hyper.notice_location_weight
        found_location = found_notice.found_location
        lost_locations = lost_notice.lost_location['locations']

        for lost_location in lost_locations:
            if lost_location['name'] == found_location['name']:
                match_degree += matching_hyper.notice_location_weight
                break

    logging.info(f"places: {match_degree} / {base} = {match_degree/base}")

    # time
    if lost_notice.est_lost_start_datetime is not None and found_notice.found_datetime is not None:
        if lost_notice.est_lost_start_datetime > found_notice.found_datetime:
            base += matching_hyper.notice_mismatched_time_weight * 2*(sigmoid((lost_notice.est_lost_start_datetime - found_notice.found_datetime).days) - 0.5)
        elif (found_notice.found_datetime - lost_notice.est_lost_end_datetime).days <= 5:
            match_degree += matching_hyper.notice_time_weight
            base += matching_hyper.notice_time_weight
        else:
            match_degree += matching_hyper.notice_time_weight * (1 - 2*(sigmoid((found_notice.found_datetime - lost_notice.est_lost_end_datetime).days - 5) - 0.5))
            base += matching_hyper.notice_time_weight

    logging.info(f"time: {match_degree} / {base} = {match_degree/base}")

    # notice description
    found_notice_desc = None
    if found_notice.description is not None:
        found_notice_desc = jieba.lcut(found_notice.description)

    lost_notice_desc = None
    if lost_notice.description is not None:
        lost_notice_desc = jieba.lcut(lost_notice.description)

    if found_notice_desc is not None and lost_notice_desc is not None:
        desc_matching_degree = matching_hyper.notice_desc_weight * word_matching_num(found_notice_desc, lost_notice_desc)
        base += desc_matching_degree
        match_degree += desc_matching_degree

    logging.info(f"notice desc: {match_degree} / {base} = {match_degree/base}")

    # notice extra
    if lost_notice.extra is not None and found_notice.extra is not None:
        extra_matching_degree = matching_hyper.notice_extra_weight * json_matching_num(lost_notice.extra, found_notice.extra)
        base += extra_matching_degree
        match_degree += extra_matching_degree

    logging.info(f"notice extra: {match_degree} / {base} = {match_degree/base}")

    ###########################################
    # PROPERTY
    ###########################################
    # property attributes
    property_template = found_property.template
    for key, weight in property_template.fields.items():
        base += weight
        match_degree += weight * (found_property.attributes[key] == lost_property.attributes[key])
        logging.info(f"{key}: {match_degree} / {base} = {match_degree / base}")

    # property tags
    found_tags = [tag.name for tag in found_property.tags.all()]
    lost_tags = [tag.name for tag in lost_property.tags.all()]
    tag_matching_degree = matching_hyper.prop_tag_weight * word_matching_num(found_tags, lost_tags)
    base += tag_matching_degree
    match_degree += tag_matching_degree

    logging.info(f"property tags: {match_degree} / {base} = {match_degree/base}")

    # property description
    lost_property_desc = None
    if lost_property.description is not None:
        lost_property_desc = jieba.lcut(lost_property.description)

    found_property_desc = None
    if found_property.description is not None:
        found_property_desc = jieba.lcut(found_property.description)

    if lost_property_desc is not None and found_property_desc is not None:
        property_desc_matching_degree = matching_hyper.prop_desc_weight * word_matching_num(lost_property_desc, found_property_desc)
        base += property_desc_matching_degree
        match_degree += property_desc_matching_degree

    logging.info(f"property desc: {match_degree} / {base} = {match_degree/base}")

    # property extra
    if lost_property.extra is not None and found_property.extra is not None:
        property_extra_matching_degree = matching_hyper.prop_extra_weight * word_matching_num(lost_property_desc, found_property_desc)
        base += property_extra_matching_degree
        match_degree += property_extra_matching_degree

    logging.info(f"property extra: {match_degree} / {base} = {match_degree/base}")

    return match_degree / base

