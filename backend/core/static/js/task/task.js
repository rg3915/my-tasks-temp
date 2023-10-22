const mydata = document.currentScript.dataset
const csrftoken = mydata.csrf

const app = 'task'
const model = 'task'
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

    // this.$watch('editItem.project', (newValue, oldValue) => {
    //   if (newValue) this.get_issues(newValue)
    // })

  },

  get_issues(newValue) {
    const projectId = newValue
    const urlIssue = `${baseUrl}/issue/${projectId}/`
    axios(urlIssue).then(response => this.editItem.issue = response.data)
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
    // this.open()
  },

  saveData() {
    if (!this.editItem.slug) {
      // Adiciona
      const { project: ignoredProject, issue: ignoredIssue, ...bodyData } = { ...this.editItem, project_id: this.editItem.project, issue_id: this.editItem.issue }
      axios.post(url, bodyData, { headers: headers })
        .then(response => {
          this.filteredItems = [...this.filteredItems, response.data]
          this.resetForm()
        })
    } else {
      // Edita
      const slug = this.editItem.slug
      // Remove o slug e associa o restante a bodyData
      const { slug: _, project: ignoredProject, issue: ignoredIssue, ...bodyData } = { ...this.editItem, project_id: this.editItem.project, issue_id: this.editItem.issue }
      axios.patch(`${url}${slug}/`, bodyData, { headers: headers })
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