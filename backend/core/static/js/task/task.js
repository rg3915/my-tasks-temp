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

  seconds: 0,
  isRunning: false, // usado para desabilitar todos os outros play
  timerInterval: null,

  init() {
    this.getData()
  },

  getData() {
    axios(url)
      .then(response => {
        this.filteredItems = response.data.map(item => ({ ...item, previous_hour: false, started: false, }))
      })

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
    this.editItem.previous_hour = false
    this.isEdit = true
    // this.open()
  },

  startTimer(item) {
    this.timerInterval = setInterval(() => {
      this.seconds++
    }, 1000)
    item.started = true
    this.isRunning = true
  },

  stopTimer(item) {
    clearInterval(this.timerInterval)
    item.started = false
    this.isRunning = false
    this.seconds = 0
  },

  resetTimer() {
    this.seconds = 0
    this.stopTimer()
  },

  formatTime(seconds) {
    const hours = String(Math.floor(seconds / 3600)).padStart(2, '0')
    const minutes = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0')
    const remainingSeconds = String(seconds % 60).padStart(2, '0')
    return `${hours}:${minutes}:${remainingSeconds}`
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

  startTask(item) {
    const slug = item ? item.slug : this.editItem.slug
    const previousHour = item ? item.previous_hour : this.editItem.previous_hour

    axios.get(`${url}${slug}/start/?previous_hour=${previousHour}`, { headers: headers })
      .then(response => {
        if (response.data.success) {
          (item ? item : this.editItem).started = true
        }
        this.startTimer(item)
      })
  },

  stopTask(item) {
    const slug = item ? item.slug : this.editItem.slug
    axios.get(`${url}${slug}/stop/`, { headers: headers })
      .then(response => {
        if (response.data.success) {
          (item ? item : this.editItem).started = false
        }
        this.stopTimer(item)
      })
  },

})