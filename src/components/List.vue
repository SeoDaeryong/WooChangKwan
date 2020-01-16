<template>
    <div class="container">
        <div class="row list">
            <div class="col-12">
                <div class="dropdown">
                    <button class="btn btn-block btn-outline-secondary dropdown-toggle" type="button" id="dropdownMenuButton"
                    v-on:click="viewSort = !viewSort">
                        정렬 방식
                    </button>
                    <ul class="list-group" v-if="viewSort" v-on:click="viewSort = !viewSort">
                        <li class="list-group-item"
                            :class="[ this.rsorted ? 'active' : '' ]"
                            v-on:click="sortedRate()">
                            남은 비율
                            <span class="label label-default" v-if="this.rsorted && this.rdesc">(내림차순)</span>
                            <span class="label label-default" v-if="this.rsorted && !this.rdesc">(오름차순)</span>
                        </li>
                        <li class="list-group-item"
                            :class="[ this.nsorted ? 'active' : '' ]"
                            v-on:click="sortedName()">
                            품목명
                            <span class="label label-default" v-if="this.nsorted && this.ndesc">(내림차순)</span>
                            <span class="label label-default" v-if="this.nsorted && !this.ndesc">(오름차순)</span>
                        </li>
                        <li class="list-group-item"
                            :class="[ this.csorted ? 'active' : '' ]"
                            v-on:click="sortedCount()">
                            현재 갯수
                            <span class="label label-default" v-if="this.csorted && this.cdesc">(내림차순)</span>
                            <span class="label label-default" v-if="this.csorted && !this.cdesc">(오름차순)</span>
                        </li>
                    </ul>
                    <!--<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item" v-on:click="sortedRate()">
                            남은 비율
                            <span class="label label-default" v-if="this.rsorted && this.rdesc">(내림차순)</span>
                            <span class="label label-default" v-if="this.rsorted && !this.rdesc">(오름차순)</span>
                        </a>
                        <a class="dropdown-item" v-on:click="sortedName()">
                            품목명
                            <span class="label label-default" v-if="this.nsorted && this.ndesc">(내림차순)</span>
                            <span class="label label-default" v-if="this.nsorted && !this.ndesc">(오름차순)</span>
                        </a>
                        <a class="dropdown-item" v-on:click="sortedCount()">
                            현재 갯수
                            <span class="label label-default" v-if="this.csorted && this.cdesc">(내림차순)</span>
                            <span class="label label-default" v-if="this.csorted && !this.cdesc">(오름차순)</span>
                        </a>
                    </div>-->
                </div>
            </div>
            <!-- <div class="col-8" v-on:click="sortedName()">품목명 
                <span class="label label-default" v-if="this.nsorted && this.ndesc">▲</span>
                <span class="label label-default" v-if="this.nsorted && !this.ndesc">▼</span>
            </div>
            <div class="col-4" v-on:click="sortedCount()">현재갯수 
                <span class="label label-default" v-if="this.csorted && this.cdesc">▲</span>
                <span class="label label-default" v-if="this.csorted && !this.cdesc">▼</span>
            </div>-->
        </div>
        <div class="row list" v-if="!add" v-on:click="add = !add">
            <div class="col-12">
                <h5 class="itemTitle">새로운 품목을 추가하세요</h5>
            </div>
        </div>
        <div class="row list" v-if="add">
            <div class="col-12">
                <div class="input-group">
                    <input type="text" class="form-control" v-model="addName" placeholder="추가할 품목명을 입력하세요" aria-describedby="basic-addon2">
                    <div class="input-group-append">
                    </div>
                </div>
            </div>
            <div class="col-12 data-input"></div>
            <div class="col-7">
                <i class="fas fa-box-open fa-2x"></i> (현재 갯수)
            </div>
            <div class="col-5">
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <div class="input-group-text"
                            v-on:click="addCount(-1, -1)"
                        >-</div>
                    </div>
                    <input type="number" class="form-control" id="count" pattern="\d*" placeholder="" :value="this.addList.count" />
                    <div class="input-group-append">
                        <div class="input-group-text"
                            v-on:click="addCount(-1, 1)"
                        >+</div>
                </div>
                </div>
            </div>
            <div class="col-7">
                <i class="fas fa-boxes fa-2x"></i> (목표 갯수)
            </div>
            <div class="col-5">
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <div class="input-group-text" v-on:click="addLimit(-1, -1)">-</div>
                    </div>
                    <input type="number" class="form-control" id="limit" pattern="\d*" placeholder="" :value="this.addList.limit" />
                    <div class="input-group-append">
                        <div class="input-group-text" v-on:click="addLimit(-1, 1)">+</div>
                    </div>
                </div>
            </div>
            <div class="col-6">
                <button type="button" class="btn btn-secondary btn-block" v-on:click="addItem()">추가</button>
            </div>
            <div class="col-6">
                <button type="button" class="btn btn-secondary btn-block" v-on:click="clearAddItem()">취소</button>
            </div>
        </div>
        <div v-for="(item, index) in this.itemList"
            class="row list">
            <div class="col-4">
                <div class="progress"
                    :data-percentage="rate(item)">
                    <span class="progress-left">
                        <span class="progress-bar" :style="progressStyle(item)"></span>
                    </span>
                    <span class="progress-right">
                        <span class="progress-bar" :style="progressStyle(item)"></span>
                    </span>
                    <div class="progress-value">
                        <div>
                            {{ item.count }} / {{ item.limit }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-1"></div>
            <div class="col-7"
                :class=""
                ><h5 class="itemTitle" v-on:click="item.viewDetail = !item.viewDetail">{{ item.name }} <!--<span class="badge">{{ item.limit }}</span>--></h5>
                <div class="row">
                    <div class="col-4">
                        <i class="fas fa-box-open fa-2x"></i>
                    </div>
                    <div class="col-8">
                        <div class="input-group mb-3">
                            <div class="input-group-prepend">
                                <span class="input-group-text"
                                    v-on:click="addCount(item.id, -1)"
                                >-</span>
                            </div>
                            <input type="number" class="form-control" id="count" pattern="\d*" placeholder="" :value="item.count"/>
                            <div class="input-group-append">
                                <span class="input-group-text"
                                    v-on:click="addCount(item.id, 1)"
                                >+</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-0"></div>
                    <div class="col-4">
                        <i class="fas fa-boxes fa-2x"></i>
                    </div>
                    <div class="col-8">
                        <div class="input-group mb-3">
                            <div class="input-group-prepend">
                                <span class="input-group-text"
                                    v-on:click="addLimit(item.id, -1)"
                                >-</span>
                            </div>
                            <input type="number" class="form-control" id="count" pattern="\d*" placeholder="" :value="item.limit"/>
                            <div class="input-group-append">
                                <span class="input-group-text"
                                    v-on:click="addLimit(item.id, 1)"
                                >+</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-0"></div>
                </div>
            </div>
            <!-- <div class="col-12">
                <div class="progress">
                    <div class="progress-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" 
                        :class="progressClass(item)"
                        :aria-valuenow="60"
                        v-bind:style="{ width: rate(item)+'%' }">
                        {{ rate(item) }}%
                    </div>
                </div>
            </div>-->
            <div class="col-12" v-if="item.viewDetail">
                <button type="button" class="btn btn-danger btn-block" v-on:click="deleteItem(item.id)">품목 삭제</button>
            </div>
        </div>

        <!--<div class="row">
            <div class="col-12 list">
                <button type="button" class="btn btn-danger" v-on:click="deleteCategory()">카테고리 삭제</button>
            </div>
        </div>-->
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'List',
  props: ['itemList', 'category'],
  components: {
  },
  data() {
    return {
      nsorted: false,
      ndsec: true,
      csorted: false,
      cdsec: true,
      rsorted: false,
      rdsec: true,
      add: false,
      viewSort: false,
      addName: "",
      addList: {
        count: 0,
        limit: 0,
      },
    }
  },
  methods: {
    addCount: function(id, value) {
      if(id < 0) {
        if(this.addList.count + value < 0) {
          this.addList.count = 0;
        } else {
          this.addList.count += value;
        }
        return 0;
      }
      var target = 0;
      for(var i = 0; i < this.itemList.length; i++) {
        if(this.itemList[i].id == id) {
          if(this.itemList[i].count + value < 0) {
            this.itemList[i].count = 0;
          } else {
            this.itemList[i].count += value;
            target = this.itemList[i].count;
          }
        }
      }
      axios.get('http://cgw01.nlp.nhnsystem.com:8300/api/item/count/' + id + '/' + target)
        .then(response => {
        })
        .catch(function (error) {
          console.log(error);
        })
    },
    addLimit: function(id, value) {
      if(id < 0) {
        if(this.addList.limit + value < 0) {
          this.addList.limit = 0;
        } else {
          this.addList.limit += value;
        }
        return 0;
      }
      var target = 0;
      for(var i = 0; i < this.itemList.length; i++) {
        if(this.itemList[i].id == id) {
          if(this.itemList[i].limit + value < 0) {
            this.itemList[i].limit = 0;
          } else {
            this.itemList[i].limit += value;
            target = this.itemList[i].limit;
          }
        }
      }
      console.log('http://cgw01.nlp.nhnsystem.com:8300/api/item/limit/' + id + '/' + target);
      axios.get('http://cgw01.nlp.nhnsystem.com:8300/api/item/limit/' + id + '/' + target)
        .then(response => {
        })
        .catch(function (error) {
          console.log(error);
        })
    },
    addItem: function() {
      var newItem = {
        name: this.addName,
        count: this.addList.count,
        limit: this.addList.limit,
        category: this.category
      };
      this.$emit("addItem", newItem);
      this.clearAddItem();
    },
    clearAddItem: function() {
      this.addList.count = 0;
      this.addList.limit = 0;
      this.addName = "";
      this.add = false;
    },
    deleteItem: function(id) {
      this.$emit("deleteItem", id);
    },
    deleteCategory: function() {
      console.log(this.category)
      this.$emit("deleteCategory", this.category);
    },
    printLine: function(item) {
      return "현재 최소갯수보다 <b>" + (item.limit - item.count) + "개</b> 부족합니다";
    },
    itemClass: function(item) {
      if(item.count >= item.limit)
        return "";
      if(item.limit - item.count < (item.limit / 2)) {
        return "warn";
      } else {
        return "danger";
      }
    },
    progressStyle: function(item) {
      var r = this.rate(item);
      if (r == 100)
        return "border-color: silver"
      else if (r > 80)
        return "border-color: dodgerblue"
      else if (r > 60)
        return "border-color: mediumseagreen"
      else if (r > 40)
        return "border-color: orange"
      else
        return "border-color: tomato"
    },
    sortedCount: function() {
      //var sortedCount = JSON.parse(JSON.stringify(this.itemList));
      var sortedCount = this.itemList;
      if(this.cdesc) {
        sortedCount.sort(function(a, b) {
          return a.count > b.count ? -1 : a.count < b.count ? 1 : 0;
        })
      } else {
        sortedCount.sort(function(a, b) {
          return a.count < b.count ? -1 : a.count > b.count ? 1 : 0;
        })
      }
      this.cdesc = !this.cdesc;
      this.csorted = true;
      this.ndesc = true;
      this.nsorted = false;
      this.rdesc = true;
      this.rsorted = false;
      return sortedCount;
    },
    sortedName: function() {
      //var sortedCount = JSON.parse(JSON.stringify(this.itemList));
      var sortedCount = this.itemList;
      if(this.ndesc) {
        sortedCount.sort(function(a, b) {
          return a.name > b.name ? -1 : a.name < b.name ? 1 : 0;
        })
      } else {
        sortedCount.sort(function(a, b) {
          return a.name < b.name ? -1 : a.name > b.name ? 1 : 0;
        })
      }
      this.ndesc = !this.ndesc;
      this.nsorted = true;
      this.cdesc = true;
      this.csorted = false;
      this.rdesc = true;
      this.rsorted = false;
      return sortedCount;
    },
    sortedRate: function() {
      //var sortedCount = JSON.parse(JSON.stringify(this.itemList));
      var sortedCount = this.itemList;
      if(this.rdesc) {
        sortedCount.sort(function(a, b) {
          return a.rate > b.rate ? -1 : a.rate < b.rate ? 1 : 0;
        })
      } else {
        sortedCount.sort(function(a, b) {
          return a.rate < b.rate ? -1 : a.rate > b.rate ? 1 : 0;
        })
      }
      this.rdesc = !this.ndesc;
      this.rsorted = true;
      this.cdesc = true;
      this.csorted = false;
      this.ndesc = true;
      this.nsorted = false;
      return sortedCount;
    },
    rate: function(item) {
      if (item.count == 0 || item.limit == 0)
        return 1;
      if (item.count > item.limit) {
        return 100;
      } else {
        return Number(((item.count / item.limit) * 100).toFixed(0));
      }
    },
    progress(event,progress,stepValue){
      //console.log(stepValue);
    },
    progress_end(event){
      //console.log("Circle progress end");
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.row {
  font-size: 12pt;
  line-height: 150%;
  font-family: "Nanum Gothic", sans-serif;
}
.list {
  text-align:center;
  vertical-align:middle;
  position: relative;
  height: 100%;
  box-shadow: 0 2px 2px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  padding: 20px 4px 20px 0px;
}

.data-input {
  padding: 10px 4px 0px 0px;
}
.col-2 {
  padding: 0px;
}

.itemTitle {
  color: Black;
  font-size: 15pt;
  font-family: "NanumBarunGothic", sans-serif;
  //font-weight: bold;
  text-decoration: underline;
}

.list:hover {
  //box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}

.detail {
  //box-shadow: 1px 1px 1px 1px rgba(158, 158, 158, 0.25);
}

.danger {
  background-color: #ff9999;
}
.warn {
  background-color: #ff9934;
}

.progress {
  width: 140px;
  height: 140px;
  line-height: 140px;
  background: none;
  margin: 0 auto;
  box-shadow: none;
  position: relative;
}
.progress:after {
  content: "";
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 7px solid #eee;
  position: absolute;
  top: 0;
  left: 0;
}
.progress > span {
  width: 50%;
  height: 100%;
  overflow: hidden;
  position: absolute;
  top: 0;
  z-index: 1;
}
.progress .progress-left {
  left: 0;
}
.progress .progress-bar {
  width: 100%;
  height: 100%;
  background: none;
  border-width: 7px;
  border-style: solid;
  position: absolute;
  top: 0;
  border-color: #ffb43e;
}
.progress .progress-left .progress-bar {
  left: 100%;
  border-top-right-radius: 75px;
  border-bottom-right-radius: 75px;
  border-left: 0;
  -webkit-transform-origin: center left;
  transform-origin: center left;
}
.progress .progress-right {
  right: 0;
}
.progress .progress-right .progress-bar {
  left: -100%;
  border-top-left-radius: 75px;
  border-bottom-left-radius: 75px;
  border-right: 0;
  -webkit-transform-origin: center right;
  transform-origin: center right;
}
.progress .progress-value {
  display: flex;
  border-radius: 50%;
  font-size: 25px;
  text-align: center;
  line-height: 20px;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-weight: 300;
}
.progress .progress-value div {
  margin-top: 0px;
  margin-left: 40px;
}
.progress .progress-value span {
  font-size: 12px;
  text-transform: uppercase;
}

/* This for look creates the    necessary css animation names 
Due to the split circle of progress-left and progress right, we must use the animations on each side. 
*/
.progress[data-percentage="1"] .progress-right .progress-bar {
  animation: loading-1 0.1s linear forwards;
}
.progress[data-percentage="1"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="2"] .progress-right .progress-bar {
  animation: loading-2 0.1s linear forwards;
}
.progress[data-percentage="2"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="3"] .progress-right .progress-bar {
  animation: loading-3 0.1s linear forwards;
}
.progress[data-percentage="3"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="4"] .progress-right .progress-bar {
  animation: loading-4 0.1s linear forwards;
}
.progress[data-percentage="4"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="5"] .progress-right .progress-bar {
  animation: loading-5 0.1s linear forwards;
}
.progress[data-percentage="5"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="6"] .progress-right .progress-bar {
  animation: loading-6 0.1s linear forwards;
}
.progress[data-percentage="6"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="7"] .progress-right .progress-bar {
  animation: loading-7 0.1s linear forwards;
}
.progress[data-percentage="7"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="8"] .progress-right .progress-bar {
  animation: loading-8 0.1s linear forwards;
}
.progress[data-percentage="8"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="9"] .progress-right .progress-bar {
  animation: loading-9 0.1s linear forwards;
}
.progress[data-percentage="9"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="10"] .progress-right .progress-bar {
  animation: loading-10 0.1s linear forwards;
}
.progress[data-percentage="10"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="11"] .progress-right .progress-bar {
  animation: loading-11 0.1s linear forwards;
}
.progress[data-percentage="11"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="12"] .progress-right .progress-bar {
  animation: loading-12 0.1s linear forwards;
}
.progress[data-percentage="12"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="13"] .progress-right .progress-bar {
  animation: loading-13 0.1s linear forwards;
}
.progress[data-percentage="13"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="14"] .progress-right .progress-bar {
  animation: loading-14 0.1s linear forwards;
}
.progress[data-percentage="14"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="15"] .progress-right .progress-bar {
  animation: loading-15 0.1s linear forwards;
}
.progress[data-percentage="15"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="16"] .progress-right .progress-bar {
  animation: loading-16 0.1s linear forwards;
}
.progress[data-percentage="16"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="17"] .progress-right .progress-bar {
  animation: loading-17 0.1s linear forwards;
}
.progress[data-percentage="17"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="18"] .progress-right .progress-bar {
  animation: loading-18 0.1s linear forwards;
}
.progress[data-percentage="18"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="19"] .progress-right .progress-bar {
  animation: loading-19 0.1s linear forwards;
}
.progress[data-percentage="19"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="20"] .progress-right .progress-bar {
  animation: loading-20 0.1s linear forwards;
}
.progress[data-percentage="20"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="21"] .progress-right .progress-bar {
  animation: loading-21 0.1s linear forwards;
}
.progress[data-percentage="21"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="22"] .progress-right .progress-bar {
  animation: loading-22 0.1s linear forwards;
}
.progress[data-percentage="22"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="23"] .progress-right .progress-bar {
  animation: loading-23 0.1s linear forwards;
}
.progress[data-percentage="23"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="24"] .progress-right .progress-bar {
  animation: loading-24 0.1s linear forwards;
}
.progress[data-percentage="24"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="25"] .progress-right .progress-bar {
  animation: loading-25 0.1s linear forwards;
}
.progress[data-percentage="25"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="26"] .progress-right .progress-bar {
  animation: loading-26 0.1s linear forwards;
}
.progress[data-percentage="26"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="27"] .progress-right .progress-bar {
  animation: loading-27 0.1s linear forwards;
}
.progress[data-percentage="27"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="28"] .progress-right .progress-bar {
  animation: loading-28 0.1s linear forwards;
}
.progress[data-percentage="28"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="29"] .progress-right .progress-bar {
  animation: loading-29 0.1s linear forwards;
}
.progress[data-percentage="29"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="30"] .progress-right .progress-bar {
  animation: loading-30 0.1s linear forwards;
}
.progress[data-percentage="30"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="31"] .progress-right .progress-bar {
  animation: loading-31 0.1s linear forwards;
}
.progress[data-percentage="31"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="32"] .progress-right .progress-bar {
  animation: loading-32 0.1s linear forwards;
}
.progress[data-percentage="32"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="33"] .progress-right .progress-bar {
  animation: loading-33 0.1s linear forwards;
}
.progress[data-percentage="33"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="34"] .progress-right .progress-bar {
  animation: loading-34 0.1s linear forwards;
}
.progress[data-percentage="34"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="35"] .progress-right .progress-bar {
  animation: loading-35 0.1s linear forwards;
}
.progress[data-percentage="35"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="36"] .progress-right .progress-bar {
  animation: loading-36 0.1s linear forwards;
}
.progress[data-percentage="36"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="37"] .progress-right .progress-bar {
  animation: loading-37 0.1s linear forwards;
}
.progress[data-percentage="37"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="38"] .progress-right .progress-bar {
  animation: loading-38 0.1s linear forwards;
}
.progress[data-percentage="38"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="39"] .progress-right .progress-bar {
  animation: loading-39 0.1s linear forwards;
}
.progress[data-percentage="39"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="40"] .progress-right .progress-bar {
  animation: loading-40 0.1s linear forwards;
}
.progress[data-percentage="40"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="41"] .progress-right .progress-bar {
  animation: loading-41 0.1s linear forwards;
}
.progress[data-percentage="41"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="42"] .progress-right .progress-bar {
  animation: loading-42 0.1s linear forwards;
}
.progress[data-percentage="42"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="43"] .progress-right .progress-bar {
  animation: loading-43 0.1s linear forwards;
}
.progress[data-percentage="43"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="44"] .progress-right .progress-bar {
  animation: loading-44 0.1s linear forwards;
}
.progress[data-percentage="44"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="45"] .progress-right .progress-bar {
  animation: loading-45 0.1s linear forwards;
}
.progress[data-percentage="45"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="46"] .progress-right .progress-bar {
  animation: loading-46 0.1s linear forwards;
}
.progress[data-percentage="46"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="47"] .progress-right .progress-bar {
  animation: loading-47 0.1s linear forwards;
}
.progress[data-percentage="47"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="48"] .progress-right .progress-bar {
  animation: loading-48 0.1s linear forwards;
}
.progress[data-percentage="48"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="49"] .progress-right .progress-bar {
  animation: loading-49 0.1s linear forwards;
}
.progress[data-percentage="49"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="50"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="50"] .progress-left .progress-bar {
  animation: 0;
}

.progress[data-percentage="51"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="51"] .progress-left .progress-bar {
  animation: loading-1 0.1s linear forwards 0.1s;
}

.progress[data-percentage="52"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="52"] .progress-left .progress-bar {
  animation: loading-2 0.1s linear forwards 0.1s;
}

.progress[data-percentage="53"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="53"] .progress-left .progress-bar {
  animation: loading-3 0.1s linear forwards 0.1s;
}

.progress[data-percentage="54"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="54"] .progress-left .progress-bar {
  animation: loading-4 0.1s linear forwards 0.1s;
}

.progress[data-percentage="55"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="55"] .progress-left .progress-bar {
  animation: loading-5 0.1s linear forwards 0.1s;
}

.progress[data-percentage="56"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="56"] .progress-left .progress-bar {
  animation: loading-6 0.1s linear forwards 0.1s;
}

.progress[data-percentage="57"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="57"] .progress-left .progress-bar {
  animation: loading-7 0.1s linear forwards 0.1s;
}

.progress[data-percentage="58"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="58"] .progress-left .progress-bar {
  animation: loading-8 0.1s linear forwards 0.1s;
}

.progress[data-percentage="59"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="59"] .progress-left .progress-bar {
  animation: loading-9 0.1s linear forwards 0.1s;
}

.progress[data-percentage="60"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="60"] .progress-left .progress-bar {
  animation: loading-10 0.1s linear forwards 0.1s;
}

.progress[data-percentage="61"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="61"] .progress-left .progress-bar {
  animation: loading-11 0.1s linear forwards 0.1s;
}

.progress[data-percentage="62"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="62"] .progress-left .progress-bar {
  animation: loading-12 0.1s linear forwards 0.1s;
}

.progress[data-percentage="63"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="63"] .progress-left .progress-bar {
  animation: loading-13 0.1s linear forwards 0.1s;
}

.progress[data-percentage="64"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="64"] .progress-left .progress-bar {
  animation: loading-14 0.1s linear forwards 0.1s;
}

.progress[data-percentage="65"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="65"] .progress-left .progress-bar {
  animation: loading-15 0.1s linear forwards 0.1s;
}

.progress[data-percentage="66"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="66"] .progress-left .progress-bar {
  animation: loading-16 0.1s linear forwards 0.1s;
}

.progress[data-percentage="67"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="67"] .progress-left .progress-bar {
  animation: loading-17 0.1s linear forwards 0.1s;
}

.progress[data-percentage="68"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="68"] .progress-left .progress-bar {
  animation: loading-18 0.1s linear forwards 0.1s;
}

.progress[data-percentage="69"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="69"] .progress-left .progress-bar {
  animation: loading-19 0.1s linear forwards 0.1s;
}

.progress[data-percentage="70"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="70"] .progress-left .progress-bar {
  animation: loading-20 0.1s linear forwards 0.1s;
}

.progress[data-percentage="71"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="71"] .progress-left .progress-bar {
  animation: loading-21 0.1s linear forwards 0.1s;
}

.progress[data-percentage="72"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="72"] .progress-left .progress-bar {
  animation: loading-22 0.1s linear forwards 0.1s;
}

.progress[data-percentage="73"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="73"] .progress-left .progress-bar {
  animation: loading-23 0.1s linear forwards 0.1s;
}

.progress[data-percentage="74"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="74"] .progress-left .progress-bar {
  animation: loading-24 0.1s linear forwards 0.1s;
}

.progress[data-percentage="75"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="75"] .progress-left .progress-bar {
  animation: loading-25 0.1s linear forwards 0.1s;
}

.progress[data-percentage="76"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="76"] .progress-left .progress-bar {
  animation: loading-26 0.1s linear forwards 0.1s;
}

.progress[data-percentage="77"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="77"] .progress-left .progress-bar {
  animation: loading-27 0.1s linear forwards 0.1s;
}

.progress[data-percentage="78"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="78"] .progress-left .progress-bar {
  animation: loading-28 0.1s linear forwards 0.1s;
}

.progress[data-percentage="79"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="79"] .progress-left .progress-bar {
  animation: loading-29 0.1s linear forwards 0.1s;
}

.progress[data-percentage="80"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="80"] .progress-left .progress-bar {
  animation: loading-30 0.1s linear forwards 0.1s;
}

.progress[data-percentage="81"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="81"] .progress-left .progress-bar {
  animation: loading-31 0.1s linear forwards 0.1s;
}

.progress[data-percentage="82"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="82"] .progress-left .progress-bar {
  animation: loading-32 0.1s linear forwards 0.1s;
}

.progress[data-percentage="83"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="83"] .progress-left .progress-bar {
  animation: loading-33 0.1s linear forwards 0.1s;
}

.progress[data-percentage="84"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="84"] .progress-left .progress-bar {
  animation: loading-34 0.1s linear forwards 0.1s;
}

.progress[data-percentage="85"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="85"] .progress-left .progress-bar {
  animation: loading-35 0.1s linear forwards 0.1s;
}

.progress[data-percentage="86"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="86"] .progress-left .progress-bar {
  animation: loading-36 0.1s linear forwards 0.1s;
}

.progress[data-percentage="87"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="87"] .progress-left .progress-bar {
  animation: loading-37 0.1s linear forwards 0.1s;
}

.progress[data-percentage="88"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="88"] .progress-left .progress-bar {
  animation: loading-38 0.1s linear forwards 0.1s;
}

.progress[data-percentage="89"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="89"] .progress-left .progress-bar {
  animation: loading-39 0.1s linear forwards 0.1s;
}

.progress[data-percentage="90"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="90"] .progress-left .progress-bar {
  animation: loading-40 0.1s linear forwards 0.1s;
}

.progress[data-percentage="91"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="91"] .progress-left .progress-bar {
  animation: loading-41 0.1s linear forwards 0.1s;
}

.progress[data-percentage="92"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="92"] .progress-left .progress-bar {
  animation: loading-42 0.1s linear forwards 0.1s;
}

.progress[data-percentage="93"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="93"] .progress-left .progress-bar {
  animation: loading-43 0.1s linear forwards 0.1s;
}

.progress[data-percentage="94"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="94"] .progress-left .progress-bar {
  animation: loading-44 0.1s linear forwards 0.1s;
}

.progress[data-percentage="95"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="95"] .progress-left .progress-bar {
  animation: loading-45 0.1s linear forwards 0.1s;
}

.progress[data-percentage="96"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="96"] .progress-left .progress-bar {
  animation: loading-46 0.1s linear forwards 0.1s;
}

.progress[data-percentage="97"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="97"] .progress-left .progress-bar {
  animation: loading-47 0.1s linear forwards 0.1s;
}

.progress[data-percentage="98"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="98"] .progress-left .progress-bar {
  animation: loading-48 0.1s linear forwards 0.1s;
}

.progress[data-percentage="99"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="99"] .progress-left .progress-bar {
  animation: loading-49 0.1s linear forwards 0.1s;
}

.progress[data-percentage="100"] .progress-right .progress-bar {
  animation: loading-50 0.1s linear forwards;
}
.progress[data-percentage="100"] .progress-left .progress-bar {
  animation: loading-50 0.1s linear forwards 0.1s;
}

@keyframes loading-1 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(3.6);
    transform: rotate(3.6deg);
  }
}
@keyframes loading-2 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(7.2);
    transform: rotate(7.2deg);
  }
}
@keyframes loading-3 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(10.8);
    transform: rotate(10.8deg);
  }
}
@keyframes loading-4 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(14.4);
    transform: rotate(14.4deg);
  }
}
@keyframes loading-5 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(18);
    transform: rotate(18deg);
  }
}
@keyframes loading-6 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(21.6);
    transform: rotate(21.6deg);
  }
}
@keyframes loading-7 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(25.2);
    transform: rotate(25.2deg);
  }
}
@keyframes loading-8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(28.8);
    transform: rotate(28.8deg);
  }
}
@keyframes loading-9 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(32.4);
    transform: rotate(32.4deg);
  }
}
@keyframes loading-10 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(36);
    transform: rotate(36deg);
  }
}
@keyframes loading-11 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(39.6);
    transform: rotate(39.6deg);
  }
}
@keyframes loading-12 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(43.2);
    transform: rotate(43.2deg);
  }
}
@keyframes loading-13 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(46.8);
    transform: rotate(46.8deg);
  }
}
@keyframes loading-14 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(50.4);
    transform: rotate(50.4deg);
  }
}
@keyframes loading-15 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(54);
    transform: rotate(54deg);
  }
}
@keyframes loading-16 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(57.6);
    transform: rotate(57.6deg);
  }
}
@keyframes loading-17 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(61.2);
    transform: rotate(61.2deg);
  }
}
@keyframes loading-18 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(64.8);
    transform: rotate(64.8deg);
  }
}
@keyframes loading-19 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(68.4);
    transform: rotate(68.4deg);
  }
}
@keyframes loading-20 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(72);
    transform: rotate(72deg);
  }
}
@keyframes loading-21 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(75.6);
    transform: rotate(75.6deg);
  }
}
@keyframes loading-22 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(79.2);
    transform: rotate(79.2deg);
  }
}
@keyframes loading-23 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(82.8);
    transform: rotate(82.8deg);
  }
}
@keyframes loading-24 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(86.4);
    transform: rotate(86.4deg);
  }
}
@keyframes loading-25 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(90);
    transform: rotate(90deg);
  }
}
@keyframes loading-26 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(93.6);
    transform: rotate(93.6deg);
  }
}
@keyframes loading-27 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(97.2);
    transform: rotate(97.2deg);
  }
}
@keyframes loading-28 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(100.8);
    transform: rotate(100.8deg);
  }
}
@keyframes loading-29 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(104.4);
    transform: rotate(104.4deg);
  }
}
@keyframes loading-30 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(108);
    transform: rotate(108deg);
  }
}
@keyframes loading-31 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(111.6);
    transform: rotate(111.6deg);
  }
}
@keyframes loading-32 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(115.2);
    transform: rotate(115.2deg);
  }
}
@keyframes loading-33 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(118.8);
    transform: rotate(118.8deg);
  }
}
@keyframes loading-34 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(122.4);
    transform: rotate(122.4deg);
  }
}
@keyframes loading-35 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(126);
    transform: rotate(126deg);
  }
}
@keyframes loading-36 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(129.6);
    transform: rotate(129.6deg);
  }
}
@keyframes loading-37 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(133.2);
    transform: rotate(133.2deg);
  }
}
@keyframes loading-38 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(136.8);
    transform: rotate(136.8deg);
  }
}
@keyframes loading-39 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(140.4);
    transform: rotate(140.4deg);
  }
}
@keyframes loading-40 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(144);
    transform: rotate(144deg);
  }
}
@keyframes loading-41 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(147.6);
    transform: rotate(147.6deg);
  }
}
@keyframes loading-42 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(151.2);
    transform: rotate(151.2deg);
  }
}
@keyframes loading-43 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(154.8);
    transform: rotate(154.8deg);
  }
}
@keyframes loading-44 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(158.4);
    transform: rotate(158.4deg);
  }
}
@keyframes loading-45 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(162);
    transform: rotate(162deg);
  }
}
@keyframes loading-46 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(165.6);
    transform: rotate(165.6deg);
  }
}
@keyframes loading-47 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(169.2);
    transform: rotate(169.2deg);
  }
}
@keyframes loading-48 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(172.8);
    transform: rotate(172.8deg);
  }
}
@keyframes loading-49 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(176.4);
    transform: rotate(176.4deg);
  }
}
@keyframes loading-50 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(180);
    transform: rotate(180deg);
  }
}
</style>
