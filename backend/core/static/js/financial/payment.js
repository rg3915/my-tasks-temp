const mydata = document.currentScript.dataset
const csrftoken = mydata.csrf

const app = 'financial'
const model = 'payment'
const baseUrl = `/api/v1/${app}`
const url = `${baseUrl}/${model}/`
const headers = { "Content-Type": "application/json", "X-CSRFToken": csrftoken }

const getItems = () => ({
  search: '',
  filteredItems: [],
  editItem: {},
  isEdit: false,

  init() {
    this.getData()
  },

  getData() {
    axios(url)
      .then(response => this.filteredItems = response.data)
  },

  async searchItems() {
    if (!this.search) {
      this.getData()
      return
    }
    const response = await axios(`${url}?search=${this.search}`)
    this.filteredItems = response.data
  },

  clearSearch() {
    this.search = ''
    this.getData()
  },

  resetForm() {
    this.editItem = {}
    this.isEdit = false
    // myModal.close()
  },

  getItem(item) {
    this.editItem = { ...item }
    this.isEdit = true
    // myModal.open()
  },

  saveData() {
    if (!this.editItem.pk) {
      // Adiciona
      const { sprint: _, ...bodyData } = { ...this.editItem, sprint_id: this.editItem.sprint }
      axios.post(url, bodyData, { headers: headers })
        .then(response => {
          this.filteredItems = [...this.filteredItems, response.data]
          this.resetForm()
        })
    } else {
      // Edita
      const pk = this.editItem.pk
      // Remove o pk e associa o restante a bodyData
      const { pk: _, ...bodyData } = this.editItem
      axios.patch(`${url}${pk}/`, bodyData, { headers: headers })
        .then(response => {
          const items = [...this.filteredItems]
          const index = items.findIndex(p => p.pk == response.data.pk)
          items[index] = response.data // atualiza o item selecionado.
          this.filteredItems = items
          this.resetForm()
        })
    }
  },
})