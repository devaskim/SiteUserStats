function xhrGetRequest(url, callback) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(callback) {
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200) {
                callback(JSON.parse(this.responseText));
            }
        }
    }.bind(xhr, callback);
    xhr.open("GET", url, true);
    xhr.send();
}

let visitorComponent = {
    data() {
        return {
            apiEndpoint: "/api/v1/users",
            pagination: {
                page: 1,
                limit: 10,
                total: 0,
                sort_field: "id",
                sort_order: "desc"
            },
            pageLimits: [ 2, 5, 10, 20, 50, 100 ],
            items: []
        }
    },
    methods: {
        loadPagination() {
            let res = localStorage.getItem("__pagination");
            if (res !== null) {
                this.pagination = JSON.parse(res);
                this.pagination.page = 1;
            }
        },
        storePagination() {
            localStorage.setItem("__pagination", JSON.stringify(this.pagination));
        },
        loadData() {
            let url = this.apiEndpoint +
                      "?page=" + this.pagination.page +
                      "&limit=" + this.pagination.limit +
                      "&field=" + this.pagination.sort_field +
                      "&sort=" + this.pagination.sort_order;

            let callback = function(response) {
                this.items = response.data || [];
                this.pagination.page = response.page || 1;
                this.pagination.limit = response.limit || 10;
                this.pagination.total = response.total || 0;
            }.bind(this);
            xhrGetRequest(url, callback);
        },
        toggleSortingOrder(field) {
            this.pagination.sort_order = this.pagination.sort_order === "asc" ? "desc" : "asc";
            this.pagination.sort_field = field;
            this.loadData();
            this.storePagination();
        },
        changeLimit() {
            this.pagination.page = 1;
            this.loadData();
            this.storePagination();
        },
        nextPage() {
            this.pagination.page++;
            this.loadData();
        },
        prevPage() {
            this.pagination.page--;
            this.loadData();
        }
    },
    created() {
        this.loadPagination();
        this.loadData();
    },
    computed: {
        pageCount() {
            return Math.ceil(this.pagination.total / this.pagination.limit);
        }
    },
    template: `<div>
                   <table class="table">
                       <thead>
                           <th @click="toggleSortingOrder('id')">id</th>
                           <th @click="toggleSortingOrder('ip')">ip</th>
                           <th @click="toggleSortingOrder('os')">os</th>
                           <th @click="toggleSortingOrder('url')">url</th>
                           <th @click="toggleSortingOrder('duration')">duration, ms</th>
                           <th>&nbsp;</th>
                       </thead>
                       <tbody>
                           <tr v-for="(item, index) in items">
                               <td>{{ item.id }}</td>
                               <td>{{ item.ip }}</td>
                               <td>{{ item.os }}</td>
                               <td>{{ item.url }}</td>
                               <td>{{ item.duration }}</td>
                               <td>
                                   <div class="modal-details">
                                       <details>
                                           <summary>Details</summary>
                                           <div class="cmc">
                                               <div class="cmt">
                                                   <p><b>ID:</b> {{ item.id }}</p>
                                                   <p><b>IP:</b> {{ item.ip }}</p>
                                                   <p><b>OS:</b> {{ item.os }}</p>
                                                   <p><b>URL:</b> {{ item.url }}</p>
                                                   <p><b>DURATION:</b> {{ item.duration }} ms</p>
                                                   <p><b>LANG:</b> {{ item.lang }}</p>
                                                   <p><b>TIMEZONE:</b> {{ item.timezone }}</p>
                                                   <p><b>AGENT:</b> {{ item.agent }}</p>
                                                   <p><b>RESOLUTION:</b> {{ item.resolution }}</p>
                                               </div>
                                           </div>
                                       </details>
                                   </div>
                               </td>
                           </tr>
                       </tbody>
                   </table>
                   <select v-model="pagination.limit" @click="changeLimit">
                       <option v-for="item in pageLimits">{{ item }}</option>
                   </select>
                   <button
                       :disabled="pagination.page === 1"
                       @click="prevPage">
                       Previous
                   </button>
                   <button
                       :disabled="pagination.page >= pageCount"
                       @click="nextPage">
                       Next
                   </button>
              </div>`
};

new Vue({
    el: "#app",
    components: {
        "visitors": visitorComponent
    }
})