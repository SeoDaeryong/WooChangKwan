import os
import sys
import json

DIR="/home1/irteam/user/seodaeryong/work/news_briefing/demo/data/topic/naver"

#'history/{}_history.json'.format(d)
#Json 파일임
def load_history(date):
    with open(os.path.join(DIR, "history/%s_history.json" % (date)), "r") as f:
        cid_history_list = json.load(f)

    history = {}
    for hlist in cid_history_list:
        history[hlist['cid']] = {
                                 "count": len(hlist["histories"]),
                                 "doc": hlist["histories"]
                               }

    return history

#카테고리[탭]리스트
def load_clustering(date):
    section_ranking = {}
    for line in open(os.path.join(DIR, "date.%s/sim-0.55/clustering-rank.txt" % (date))):
        line = line.strip().split("\t")
        section_ranking[line[0]] = eval(line[1])

    return section_ranking

def append_doc(clusters, doc):
    clusters.append(
                {
                    "title": doc["title"],
                    "office_name": doc["office_name"],
                    "link": doc["link"],
                })
    if "paper_info" in doc:
        clusters[-1]["paper_info"] = doc["paper_info"]

#Json 파일임
def load_document(date):
    with open(os.path.join(DIR, "date.%s/sim-0.55/clustering-issue.j" % (date)), "r", encoding='utf-8') as f:
        cid_cluster = json.load(f)

    clusters = {}
    for sub in cid_cluster:
        clusters[sub["cid"]] = {
                                 #"comment_count": sub["comment_count"],
                                 "doc_count": sub["doc_count"],
                                 "docs": [],
                               }
        comment_cnt = int(sub["issue_doc"]["commentCount"])
        append_doc(clusters[sub["cid"]]["docs"], sub["issue_doc"])
        if "issue_docs" in sub:
            for doc in sub["issue_docs"]:
                append_doc(clusters[sub["cid"]]["docs"], doc)
                comment_cnt += int(doc["commentCount"])

        if "docs" in sub:
            for doc in sub["docs"]:
                comment_cnt += int(doc["commentCount"])

        clusters[sub["cid"]]["comment_count"] = comment_cnt

    return clusters

def load_stat(date):
    tmp = {}
    with open(os.path.join(DIR, "date.%s/sim-0.55/clustering-stat.txt" % (date)), "r", encoding='utf-8') as f:
        tmp = json.load(f)

    stat = {}
    for s in tmp:
        stat[s['cid']] = s

    return stat

def load_video_info(date):
    video = {}
    for line in open(os.path.join(DIR, "date.%s/sim-0.55/youtube-issue.txt" % (date))):
        line = line.strip().split("\t")
        video[line[0]] = json.loads(line[1])

    return video


#카테고리[탭]사전형식
def load_summary(date):
    cid_summary = {}
    for line in open(os.path.join(DIR, "summary/%s.issue.summary.json" % (date))):
        line = line.strip().split("\t")
        cid_summary[line[0]] = eval(line[1])

    return cid_summary

if __name__ == "__main__":
    date="20190726"
    #print(load_history(date))
    print(load_clustering_rank(date))
    clusters = load_cluster(date)
    print(json.dumps(clusters, indent=4, sort_keys=True))
    #print(load_summary(date))
