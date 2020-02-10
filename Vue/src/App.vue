<template>
    <div id="app">
        <div class="container">
            <div class="row" style="margin: 10px; box-shadow: 0 2px 0px 0 rgba(0,0,0,0.2);">
                <div class="col-12">
                    <a href='/'><h2 class="title" v-html="title"></h2></a>
                </div>
            </div>
        </div>
        <Category
          :category="pushPlus()"
          :perView="calPerView()"
          :tgtCategory="selectCtg"
          v-on:changeItem="changeItem"
          v-on:addCategory="addCtg"
          v-on:deleteCategory="deleteCategory"
          :key="categoryKey"
        ></Category>
        <List
          :itemList="viewItemList()"
          :category="selectCtg"
          v-on:addItem="addItem"
          v-on:deleteItem="deleteItem"
        ></List>
    </div>
</template>

<script>
import Category from './components/Category'
import List from './components/List'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Category,
    List
  },
  data() {
    return {
      title : '<font class="cap">우</font>리집 <font class="cap">창</font>고 <font class="cap">관</font>리인',
      categoryKey: 1,
      category : [
      ],
      selectCtg: "",
      itemList: [
        {
          id: 1,
          name: "name1",
          count: 10,
          limit: 5,
          edit: false,
          viewDetail: false
        },
        {
          id: 2,
          name: "name2",
          count: 3,
          limit: 5,
          edit: false,
          viewDetail: false
        }
      ],
    }
  },
  created() {
    this.getCategoryAndItem();
  },
  methods: {
    getCategoryAndItem: function() {
      axios.get('http://cgw01.nlp.nhnsystem.com:8300/api/category')
        .then(response => {
          var tmp = [];
          for(var i in response.data) {
            tmp.push(response.data[i]);
          }
          this.category = tmp;
          this.selectCtg = tmp[0].category;
          this.getItem();
        })
        .catch(function (error) {
          console.log(error);
        })
    },
    getItem: function() {
      axios.get('http://cgw01.nlp.nhnsystem.com:8300/api/item?category=' + this.selectCtg)
        .then(response => {
        var tmp = [];
        for(var i in response.data) {
          response.data[i].edit = false;
          response.data[i].viewDetail = false;
          response.data[i].rate = Number(((response.data[i].count / response.data[i].limit) * 100).toFixed(0));
          tmp.push(response.data[i]);
        }
        this.itemList = tmp;
      })
      .catch(function (error) {
        console.log(error);
      })
    },
    addCtg: function(newCategory) {
      axios.post('http://cgw01.nlp.nhnsystem.com:8300/api/category', {
          category: newCategory,
          order: this.category.length + 1
        })
        .then(response => {
          var tmp = [];
          for(var i in response.data) {
            tmp.push(response.data[i]);
          }
          this.category = tmp;
        })
        .catch(function (error) {
          console.log(error);
        })
      this.categoryKey += 1;
    },
    addItem: function(newItem) {
      console.log(newItem);
      axios.post('http://cgw01.nlp.nhnsystem.com:8300/api/item', newItem)
        .then(response => {
          this.getItem();
        })
        .catch(function (error) {
          console.log(error);
        })
    },
    deleteItem: function(id) {
      axios.get('http://cgw01.nlp.nhnsystem.com:8300/api/item/' + id)
        .then(response => {
            this.getItem();
        })
        .catch(function (error) {
          console.log(error);
        })
    },
    deleteCategory: function(ctg) {
      var id = -1;
      for(var i = 0; i < this.category.length; i++) {
        if(this.category[i].category == ctg) {
          id = this.category[i].id;
          break;
        }
      }
      console.log('http://cgw01.nlp.nhnsystem.com:8300/api/category/' + id);
      axios.get('http://cgw01.nlp.nhnsystem.com:8300/api/category/' + id)
        .then(response => {
          this.getCategoryAndItem();
        })
        .catch(function (error) {
          console.log(error);
        })
    },
    changeItem: function(category) {
      this.selectCtg = category
      axios.get('http://cgw01.nlp.nhnsystem.com:8300/api/item?category=' + category)
        .then(response => {
        this.getItem();
      })
      .catch(function (error) {
        console.log(error);
      })
    },
    pushPlus: function() {
      return this.category;
    },
    calPerView: function() {
      //this.categoryKey += 1;
      return this.category.length+1 > 5 ? 5 : 5;
    },
    viewItemList: function() {
      return this.itemList;
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  //margin-top: 20px;
  //display: flex;
  align-items: center;
  flex-direction: column;
  height: 100%;
}

.cap {
  color: Black;
  font-size: 20pt;
  font-weight: bold;
}

.title {
  color: Gray;
  font-size: 15pt;
  font-family: "나눔 고딕", sans-serif;
  font-weight: bold;
}

</style>
