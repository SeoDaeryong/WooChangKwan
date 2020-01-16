<template>
    <div class="container">
        <swiper :options="swiperOptions">
            <swiper-slide v-for="(c, index) in category" :key="index">
                <button type="button" class="btn btn-dark" v-if="!add && tgtCategory == c.category" v-on:click="viewCategoryDelete = !viewCategoryDelete">{{ c.category }}</button>
                <button type="button" class="btn btn-outline-dark" v-if="add || tgtCategory != c.category" v-on:click="changeItem(c.category)">{{ c.category }}</button>
            </swiper-slide>
            <swiper-slide >
                <button type="button" class="btn btn-outline-dark" v-if="!viewDetail" v-on:click="viewDetail = !viewDetail"><i class="fas fa-angle-down"></i></button>
                <button type="button" class="btn btn-outline-dark" v-if="viewDetail" v-on:click="viewDetail = !viewDetail"><i class="fas fa-angle-up"></i></button>
            </swiper-slide>
            <div class="swiper-pagination" slot="pagination"></div>
        </swiper>
        <div class="row list" v-if="viewCategoryDelete">
            <div class="col-12">
                <button type="button" class="btn btn-danger btn-block" v-on:click="deleteCategory()">카테고리 삭제</button>
            </div>
        </div>
        <div class="row list" v-if="viewDetail">
            <div class="col-6">
                <button type="button" class="btn btn-block btn-secondary" v-on:click="viewSort = !viewSort"> 카테고리 정렬 </button>
            </div>
            <div class="col-6">
                <button type="button" class="btn btn-block btn-dark" v-on:click="add = !add"> 카테고리 추가 </button>
            </div>
        </div>
        <div class="row" v-if="viewSort">
            <div class="col-12 list">
                <draggable
                    :list="category"
                    group="wck"
                    ghost-class="ghost"
                    @start="drag=true"
                    @end="dragEnd">
                    <span v-for="(c, index) in category" :key="index">
                        <button type="button" class="sctg btn btn-dark">{{ c.category }}</button>
                    </span>
                </draggable>
            </div>
        </div>
        <div class="row" v-if="add">
            <hr>
            <div class="col-12 list">
                <div class="input-group">
                    <input type="text" class="form-control" v-model="newCategory" placeholder="카테고리명을 입력하세요" aria-describedby="basic-addon2">
                    <div class="input-group-append">
                        <span class="btn btn-outline-secondary" id="basic-addon2" v-on:click="addCategory()">추가</span>
                        <span class="btn btn-outline-secondary" id="basic-addon2" v-on:click="clearCategory()">취소</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Movie from './Movie'
import 'swiper/dist/css/swiper.css'
import { swiper, swiperSlide } from 'vue-awesome-swiper'
import Draggable from "vuedraggable";
import axios from "axios";

export default {
  name: 'Category',
  props: ['category', 'perView', 'tgtCategory'],
  components: {
    Movie,
    swiper,
    swiperSlide,
    Draggable
  },
  data() {
    return {
      add: false,
      newCategory: "",
      viewCategoryDelete: false,
      viewSort: false,
      viewDetail: false,
      swiperOptions : {
        slidesPerView: this.perView,
        spaceBetween: 0,
        freeMode: false,
        loop: false,
        navigation: {
          //nextEl: '.swiper-button-next',
          //prevEl: '.swiper-button-prev'
        }
      }
    }
  },
  computed: {
    shouldUseDragHandle() {
      return this.isDesktop ? "" : ".drag-handle";
    }
  },
  methods: {
    addCategory: function() {
      this.$emit("addCategory", this.newCategory);
      //this.category.push(this.newCategory);
      this.clearCategory();
    },
    clearCategory: function() {
      this.add = false;
      this.newCategory = "";
    },
    changeItem: function(category) {
      this.$emit("changeItem", category);
      this.viewCategoryDelete = false;
    },
    deleteCategory: function() {
      console.log(this.tgtCategory)
      this.$emit("deleteCategory", this.tgtCategory);
      this.viewCategoryDelete = false;
    },
    dragEnd: function() {
      for(var i = 0; i < this.category.length; i++) {
        this.category[i].order = i+1;
      }
      axios.post('http://cgw01.nlp.nhnsystem.com:8300/api/category_list', this.category)
      .then(response => {
      })
      .catch(function (error) {
        console.log(error);
      })
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.swiper-slide{
  display: flex;
  justify-content: center;
  flex-direction: column;
}
.swiper-container {
  //height : 450px;
  width : 100%;
}

.list {
  text-align:center;
  vertical-align:middle;
  position: relative;
  height: 100%;
  box-shadow: 0 2px 2px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  padding: 20px 16px;
}

.sctg {
  margin: 2px 2px 2px 2px;
}

</style>
