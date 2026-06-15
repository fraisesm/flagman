<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand__logo">Ф</div>
        <div>
          <p class="brand__name">Флагман</p>
          <p class="brand__desc">Документооборот MVP</p>
        </div>
      </div>

      <div class="backend-box">
        <label>Backend URL</label>
        <input v-model="baseUrl" class="input" placeholder="http://127.0.0.1:8000" />
      </div>

      <div class="backend-box">
        <label>Последние ID</label>
        <div class="quick-ids">
          <span>user: {{ lastIds.user_id ?? '—' }}</span>
          <span>org: {{ lastIds.organization_id ?? '—' }}</span>
          <span>department: {{ lastIds.department_id ?? '—' }}</span>
          <span>document: {{ lastIds.document_id ?? '—' }}</span>
          <span>recipient: {{ lastIds.recipient_user_id ?? '—' }}</span>
        </div>
      </div>

      <nav class="nav">
        <button
          v-for="item in tabs"
          :key="item.key"
          class="nav__item"
          :class="{ active: activeTab === item.key }"
          @click="activeTab = item.key"
        >
          <span>{{ item.label }}</span>
        </button>
      </nav>

      <div class="sidebar__footer">
        <p>Все действия ниже идут в реальные backend endpoints через fetch.</p>
      </div>
    </aside>

    <main class="main">
      <header class="topbar">
        <div>
          <p class="eyebrow">Сервис рассылки и подписания документов</p>
          <h1>{{ currentTabTitle }}</h1>
        </div>

        <div class="topbar__actions">
          <button class="button button--ghost" @click="fillDemoFlow">Подставить последние ID</button>
          <button class="button button--ghost" @click="clearOutput">Очистить ответ</button>
        </div>
      </header>

      <section class="hero-card">
        <div>
          <h2>Рабочий интерфейс для защиты</h2>
          <p>
            Интерфейс покрывает текущий flow: регистрация пользователя, организация,
            отделы, приглашение, роли, создание документа, отправка, подпись,
            inbox, outbox, pending и статус документа.
          </p>
        </div>

        <div class="hero-stats">
          <div class="stat">
            <span>Backend</span>
            <strong>{{ baseUrl }}</strong>
          </div>
          <div class="stat">
            <span>Текущая вкладка</span>
            <strong>{{ currentTabTitle }}</strong>
          </div>
        </div>
      </section>

      <section v-if="activeTab === 'users'" class="content-grid">
        <article class="panel">
          <div class="panel__head">
            <h3>Регистрация пользователя</h3>
            <span class="tag">/auth/register</span>
          </div>

          <div class="form">
            <input v-model="registerForm.full_name" class="input" placeholder="ФИО" />
            <input v-model="registerForm.email" class="input" placeholder="Email" />
            <input v-model="registerForm.phone" class="input" placeholder="Телефон" />
            <input v-model="registerForm.password" class="input" type="password" placeholder="Пароль" />
            <button class="button" @click="registerUser">Зарегистрировать</button>
          </div>
        </article>
      </section>

      <section v-if="activeTab === 'structure'" class="content-grid">
        <article class="panel">
          <div class="panel__head">
            <h3>Создание организации</h3>
            <span class="tag">/organizations/create</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="fillOrganizationName">Тестовое название</button>
          </div>

          <div class="form">
            <input v-model="organizationForm.name" class="input" placeholder="Название организации" />
            <button class="button" @click="createOrganization">Создать организацию</button>
          </div>
        </article>

        <article class="panel">
          <div class="panel__head">
            <h3>Создание отдела</h3>
            <span class="tag">/departments/create</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="departmentForm.organization_id = lastIds.organization_id">Подставить org_id</button>
          </div>

          <div class="form">
            <input v-model.number="departmentForm.organization_id" class="input" type="number" placeholder="ID организации" />
            <input v-model="departmentForm.name" class="input" placeholder="Название отдела" />
            <button class="button" @click="createDepartment">Создать отдел</button>
          </div>
        </article>

        <article class="panel">
          <div class="panel__head">
            <h3>Приглашение сотрудника</h3>
            <span class="tag">/employees/invite</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="inviteForm.organization_id = lastIds.organization_id">Подставить org_id</button>
            <button class="mini-button" @click="inviteForm.user_id = lastIds.user_id">Подставить user_id</button>
          </div>

          <div class="form">
            <input v-model.number="inviteForm.user_id" class="input" type="number" placeholder="ID пользователя" />
            <input v-model.number="inviteForm.organization_id" class="input" type="number" placeholder="ID организации" />
            <button class="button" @click="inviteEmployee">Пригласить</button>
          </div>
        </article>

        <article class="panel">
          <div class="panel__head">
            <h3>Выдача роли</h3>
            <span class="tag">/access/assign-role</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="fillRoleIds">Подставить ID</button>
            <button class="mini-button" @click="setSenderRole">Роль отправителя</button>
            <button class="mini-button" @click="setSignerRole">Роль подписанта</button>
          </div>

          <div class="form">
            <input v-model.number="roleForm.user_id" class="input" type="number" placeholder="ID пользователя" />
            <input v-model.number="roleForm.organization_id" class="input" type="number" placeholder="ID организации" />
            <input v-model.number="roleForm.department_id" class="input" type="number" placeholder="ID отдела" />
            <input v-model="roleForm.role_name" class="input" placeholder="Название роли" />

            <div class="checks">
              <label class="checkbox">
                <input v-model="roleForm.can_send_document" type="checkbox" />
                <span>can_send_document</span>
              </label>

              <label class="checkbox">
                <input v-model="roleForm.can_sign_document" type="checkbox" />
                <span>can_sign_document</span>
              </label>

              <label class="checkbox">
                <input v-model="roleForm.can_manage_department" type="checkbox" />
                <span>can_manage_department</span>
              </label>
            </div>

            <button class="button" @click="assignRole">Выдать роль</button>
          </div>
        </article>
      </section>

      <section v-if="activeTab === 'documents'" class="content-grid">
        <article class="panel">
          <div class="panel__head">
            <h3>Создание документа</h3>
            <span class="tag">/documents/create</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="fillDocumentIds">Подставить ID</button>
            <button class="mini-button" @click="fillDocumentTemplate">Тестовый документ</button>
          </div>

          <div class="form">
            <input v-model="documentForm.title" class="input" placeholder="Заголовок документа" />
            <textarea v-model="documentForm.content" class="input textarea" placeholder="Содержимое документа"></textarea>
            <input v-model.number="documentForm.sender_user_id" class="input" type="number" placeholder="ID отправителя" />
            <input v-model.number="documentForm.organization_id" class="input" type="number" placeholder="ID организации" />
            <input v-model.number="documentForm.department_id" class="input" type="number" placeholder="ID отдела" />
            <button class="button" @click="createDocument">Создать документ</button>
          </div>
        </article>

        <article class="panel">
          <div class="panel__head">
            <h3>Отправка документа</h3>
            <span class="tag">/documents/send</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="fillSendIds">Подставить ID</button>
          </div>

          <div class="form">
            <input v-model.number="sendForm.document_id" class="input" type="number" placeholder="ID документа" />
            <input v-model.number="sendForm.sender_user_id" class="input" type="number" placeholder="ID отправителя" />
            <input v-model.number="sendForm.organization_id" class="input" type="number" placeholder="ID организации" />
            <input v-model.number="sendForm.department_id" class="input" type="number" placeholder="ID отдела" />
            <input v-model.number="sendForm.recipient_user_id" class="input" type="number" placeholder="ID получателя" />
            <button class="button" @click="sendDocument">Отправить документ</button>
          </div>
        </article>

        <article class="panel">
          <div class="panel__head">
            <h3>Подписание документа</h3>
            <span class="tag">/signatures/sign</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="fillSignIds">Подставить ID</button>
          </div>

          <div class="form">
            <input v-model.number="signForm.document_id" class="input" type="number" placeholder="ID документа" />
            <input v-model.number="signForm.signer_user_id" class="input" type="number" placeholder="ID подписанта" />
            <input v-model.number="signForm.organization_id" class="input" type="number" placeholder="ID организации" />
            <input v-model.number="signForm.department_id" class="input" type="number" placeholder="ID отдела" />
            <select v-model="signForm.confirmation_channel" class="input">
              <option value="sms">sms</option>
              <option value="email">email</option>
              <option value="messenger">messenger</option>
            </select>
            <button class="button" @click="signDocument">Подписать документ</button>
          </div>
        </article>
      </section>

      <section v-if="activeTab === 'lists'" class="content-grid">
        <article class="panel">
          <div class="panel__head">
            <h3>Inbox</h3>
            <span class="tag">/documents/inbox</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="inboxUserId = lastIds.user_id">Подставить user_id</button>
          </div>

          <div class="form">
            <input v-model.number="inboxUserId" class="input" type="number" placeholder="ID пользователя" />
            <button class="button button--secondary" @click="loadInbox">Загрузить входящие</button>
          </div>

          <div class="list" v-if="Array.isArray(inboxList) && inboxList.length">
            <div v-for="item in inboxList" :key="`inbox-${item.document_id}`" class="list-item">
              <strong>{{ item.title }}</strong>
              <span>ID документа: {{ item.document_id }}</span>
              <span>Статус: {{ item.status }}</span>
            </div>
          </div>

          <p v-else class="empty">Нет входящих документов</p>
        </article>

        <article class="panel">
          <div class="panel__head">
            <h3>Outbox</h3>
            <span class="tag">/documents/outbox</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="outboxUserId = lastIds.user_id">Подставить user_id</button>
          </div>

          <div class="form">
            <input v-model.number="outboxUserId" class="input" type="number" placeholder="ID пользователя" />
            <button class="button button--secondary" @click="loadOutbox">Загрузить исходящие</button>
          </div>

          <div class="list" v-if="Array.isArray(outboxList) && outboxList.length">
            <div v-for="item in outboxList" :key="`outbox-${item.document_id}`" class="list-item">
              <strong>{{ item.title }}</strong>
              <span>ID документа: {{ item.document_id }}</span>
              <span>Отправитель: {{ item.sender_user_id }}</span>
            </div>
          </div>

          <p v-else class="empty">Нет исходящих документов</p>
        </article>

        <article class="panel">
          <div class="panel__head">
            <h3>Pending</h3>
            <span class="tag">/documents/pending</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="pendingUserId = lastIds.user_id">Подставить user_id</button>
          </div>

          <div class="form">
            <input v-model.number="pendingUserId" class="input" type="number" placeholder="ID пользователя" />
            <button class="button button--secondary" @click="loadPending">Загрузить ожидающие</button>
          </div>

          <div class="list" v-if="Array.isArray(pendingList) && pendingList.length">
            <div v-for="item in pendingList" :key="`pending-${item.document_id}`" class="list-item">
              <strong>{{ item.title }}</strong>
              <span>ID документа: {{ item.document_id }}</span>
              <span>Статус: {{ item.status }}</span>
            </div>
          </div>

          <p v-else class="empty">Нет документов на подпись</p>
        </article>

        <article class="panel">
          <div class="panel__head">
            <h3>Статус документа</h3>
            <span class="tag">/documents/status/:document_id/:recipient_user_id</span>
          </div>

          <div class="inline-actions">
            <button class="mini-button" @click="fillStatusIds">Подставить ID</button>
          </div>

          <div class="form">
            <input v-model.number="statusForm.document_id" class="input" type="number" placeholder="ID документа" />
            <input v-model.number="statusForm.recipient_user_id" class="input" type="number" placeholder="ID получателя" />
            <button class="button button--secondary" @click="loadStatus">Проверить статус</button>
          </div>

          <div class="json-box">
            <pre>{{ pretty(statusResult) }}</pre>
          </div>
        </article>
      </section>

      <section class="panel output-panel">
        <div class="panel__head">
          <h3>Ответ сервера</h3>
          <span class="tag">JSON output</span>
        </div>

        <div class="json-box">
          <pre>{{ pretty(output) }}</pre>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

const baseUrl = ref('http://127.0.0.1:8000')
const activeTab = ref('users')

const tabs = [
  { key: 'users', label: 'Пользователи' },
  { key: 'structure', label: 'Структура' },
  { key: 'documents', label: 'Документы' },
  { key: 'lists', label: 'Списки и статусы' }
]

const currentTabTitle = computed(() => {
  return tabs.find((item) => item.key === activeTab.value)?.label || 'Frontend'
})

const output = ref(null)
const inboxList = ref([])
const outboxList = ref([])
const pendingList = ref([])
const statusResult = ref(null)

const inboxUserId = ref(null)
const outboxUserId = ref(null)
const pendingUserId = ref(null)

const lastIds = reactive({
  user_id: null,
  organization_id: null,
  department_id: null,
  document_id: null,
  recipient_user_id: null
})

const registerForm = reactive({
  full_name: '',
  email: '',
  phone: '',
  password: ''
})

const organizationForm = reactive({
  name: ''
})

const departmentForm = reactive({
  organization_id: null,
  name: ''
})

const inviteForm = reactive({
  user_id: null,
  organization_id: null
})

const roleForm = reactive({
  user_id: null,
  organization_id: null,
  department_id: null,
  role_name: '',
  can_send_document: false,
  can_sign_document: false,
  can_manage_department: false
})

const documentForm = reactive({
  title: '',
  content: '',
  sender_user_id: null,
  organization_id: null,
  department_id: null
})

const sendForm = reactive({
  document_id: null,
  sender_user_id: null,
  organization_id: null,
  department_id: null,
  recipient_user_id: null
})

const signForm = reactive({
  document_id: null,
  signer_user_id: null,
  organization_id: null,
  department_id: null,
  confirmation_channel: 'sms'
})

const statusForm = reactive({
  document_id: null,
  recipient_user_id: null
})

function pretty(value) {
  if (value === null || value === undefined) return 'Нет данных'
  return JSON.stringify(value, null, 2)
}

function clearOutput() {
  output.value = null
}

function normalizeError(data) {
  if (!data) return 'Неизвестная ошибка'

  if (typeof data === 'string') return data

  if (typeof data.detail === 'string') return data.detail

  if (Array.isArray(data.detail)) {
    return data.detail
      .map((item) => {
        const field = Array.isArray(item.loc) ? item.loc.join(' -> ') : 'field'
        const msg = item.msg || 'Ошибка валидации'
        return `${field}: ${msg}`
      })
      .join('\n')
  }

  if (typeof data.detail === 'object') {
    return JSON.stringify(data.detail, null, 2)
  }

  return JSON.stringify(data, null, 2)
}

function updateLastIds(data) {
  if (!data || typeof data !== 'object') return

  if ('id' in data && ('email' in data || 'full_name' in data)) {
    lastIds.user_id = data.id
  }

  if ('id' in data && 'name' in data && !('title' in data) && !('email' in data)) {
    if (organizationForm.name === data.name) {
      lastIds.organization_id = data.id
    }
  }

  if ('department_id' in data) {
    lastIds.department_id = data.department_id
  }

  if ('id' in data && 'title' in data && 'content' in data) {
    lastIds.document_id = data.id
  }

  if ('recipient_user_id' in data) {
    lastIds.recipient_user_id = data.recipient_user_id
  }
}

function fillOrganizationName() {
  organizationForm.name = 'ООО Флагман Demo'
}

function fillRoleIds() {
  roleForm.user_id = lastIds.user_id
  roleForm.organization_id = lastIds.organization_id
  roleForm.department_id = lastIds.department_id
}

function fillDocumentIds() {
  documentForm.sender_user_id = lastIds.user_id
  documentForm.organization_id = lastIds.organization_id
  documentForm.department_id = lastIds.department_id
}

function fillSendIds() {
  sendForm.document_id = lastIds.document_id
  sendForm.sender_user_id = lastIds.user_id
  sendForm.organization_id = lastIds.organization_id
  sendForm.department_id = lastIds.department_id
  sendForm.recipient_user_id = lastIds.recipient_user_id ?? lastIds.user_id
}

function fillSignIds() {
  signForm.document_id = lastIds.document_id
  signForm.signer_user_id = lastIds.recipient_user_id ?? lastIds.user_id
  signForm.organization_id = lastIds.organization_id
  signForm.department_id = lastIds.department_id
}

function fillStatusIds() {
  statusForm.document_id = lastIds.document_id
  statusForm.recipient_user_id = lastIds.recipient_user_id ?? lastIds.user_id
}

function fillDocumentTemplate() {
  documentForm.title = 'Приказ о внутреннем ознакомлении'
  documentForm.content = 'Сотруднику необходимо ознакомиться с документом и подписать его.'
}

function setSenderRole() {
  roleForm.role_name = 'sender'
  roleForm.can_send_document = true
  roleForm.can_sign_document = false
  roleForm.can_manage_department = false
}

function setSignerRole() {
  roleForm.role_name = 'signer'
  roleForm.can_send_document = false
  roleForm.can_sign_document = true
  roleForm.can_manage_department = false
}

function fillDemoFlow() {
  departmentForm.organization_id = lastIds.organization_id
  inviteForm.organization_id = lastIds.organization_id

  roleForm.organization_id = lastIds.organization_id
  roleForm.department_id = lastIds.department_id

  documentForm.organization_id = lastIds.organization_id
  documentForm.department_id = lastIds.department_id
  documentForm.sender_user_id = lastIds.user_id

  sendForm.organization_id = lastIds.organization_id
  sendForm.department_id = lastIds.department_id
  sendForm.document_id = lastIds.document_id
  sendForm.sender_user_id = lastIds.user_id
  sendForm.recipient_user_id = lastIds.recipient_user_id

  signForm.organization_id = lastIds.organization_id
  signForm.department_id = lastIds.department_id
  signForm.document_id = lastIds.document_id
  signForm.signer_user_id = lastIds.recipient_user_id

  statusForm.document_id = lastIds.document_id
  statusForm.recipient_user_id = lastIds.recipient_user_id
}

async function apiRequest(path, method = 'GET', body = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  }

  if (body) {
    options.body = JSON.stringify(body)
  }

  const response = await fetch(`${baseUrl.value}${path}`, options)

  let data
  try {
    data = await response.json()
  } catch {
    data = { detail: 'Сервер вернул не JSON' }
  }

  if (!response.ok) {
    const message = normalizeError(data)
    output.value = {
      status: response.status,
      error: message,
      raw: data
    }
    throw new Error(message)
  }

  output.value = data
  updateLastIds(data)
  return data
}

async function registerUser() {
  try {
    const data = await apiRequest('/auth/register', 'POST', registerForm)
    if (data?.id) {
      lastIds.user_id = data.id
      inviteForm.user_id = data.id
      roleForm.user_id = data.id
      documentForm.sender_user_id = data.id
    }
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function createOrganization() {
  try {
    const data = await apiRequest('/organizations/create', 'POST', organizationForm)
    if (data?.id) {
      lastIds.organization_id = data.id
      departmentForm.organization_id = data.id
      inviteForm.organization_id = data.id
      roleForm.organization_id = data.id
      documentForm.organization_id = data.id
      sendForm.organization_id = data.id
      signForm.organization_id = data.id
    }
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function createDepartment() {
  try {
    const data = await apiRequest('/departments/create', 'POST', departmentForm)
    if (data?.id) {
      lastIds.department_id = data.id
      roleForm.department_id = data.id
      documentForm.department_id = data.id
      sendForm.department_id = data.id
      signForm.department_id = data.id
    }
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function inviteEmployee() {
  try {
    const data = await apiRequest('/employees/invite', 'POST', inviteForm)
    if (inviteForm.user_id) {
      lastIds.recipient_user_id = inviteForm.user_id
      sendForm.recipient_user_id = inviteForm.user_id
      signForm.signer_user_id = inviteForm.user_id
      statusForm.recipient_user_id = inviteForm.user_id
    }
    return data
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function assignRole() {
  try {
    await apiRequest('/access/assign-role', 'POST', roleForm)
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function createDocument() {
  try {
    const data = await apiRequest('/documents/create', 'POST', documentForm)
    if (data?.id) {
      lastIds.document_id = data.id
      sendForm.document_id = data.id
      signForm.document_id = data.id
      statusForm.document_id = data.id
    }
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function sendDocument() {
  try {
    const data = await apiRequest('/documents/send', 'POST', sendForm)
    if (sendForm.recipient_user_id) {
      lastIds.recipient_user_id = sendForm.recipient_user_id
      signForm.signer_user_id = sendForm.recipient_user_id
      statusForm.recipient_user_id = sendForm.recipient_user_id
    }
    return data
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function signDocument() {
  try {
    await apiRequest('/signatures/sign', 'POST', signForm)
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function loadInbox() {
  try {
    inboxList.value = await apiRequest('/documents/inbox', 'POST', {
      user_id: inboxUserId.value
    })
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function loadOutbox() {
  try {
    outboxList.value = await apiRequest('/documents/outbox', 'POST', {
      user_id: outboxUserId.value
    })
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function loadPending() {
  try {
    pendingList.value = await apiRequest('/documents/pending', 'POST', {
      user_id: pendingUserId.value
    })
  } catch (e) {
    output.value = { error: e.message }
  }
}

async function loadStatus() {
  try {
    statusResult.value = await apiRequest(
      `/documents/status/${statusForm.document_id}/${statusForm.recipient_user_id}`,
      'GET'
    )
  } catch (e) {
    output.value = { error: e.message }
  }
}
</script>