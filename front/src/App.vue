<template>
  <div id="app" :data-theme="theme">

    <!-- ===== ЭКРАН ВХОДА ===== -->
    <transition name="fade">
      <div v-if="!token" class="auth-screen">
        <div class="auth-card">
          <div class="auth-logo">
            <svg width="40" height="40" viewBox="0 0 44 44" fill="none" aria-label="Флагман">
              <rect width="44" height="44" rx="12" fill="#1a7fc4"/>
              <path d="M10 34V10h18l-6 8h-6v16H10z" fill="white"/>
              <path d="M22 10h12l-6 8H22l6-8z" fill="white" opacity="0.6"/>
            </svg>
            <span class="auth-logo__text">Флагман</span>
          </div>
          <p class="auth-subtitle">Сервис рассылки и подписания документов</p>

          <!-- LOGIN -->
          <div v-if="authMode === 'login'" class="auth-form">
            <h2>Войти в аккаунт</h2>
            <label>Email
              <input v-model="loginForm.email" class="input" type="email" placeholder="you@company.ru" autocomplete="email" />
            </label>
            <label>Пароль
              <input v-model="loginForm.password" class="input" type="password" placeholder="••••••••" autocomplete="current-password" />
            </label>
            <details class="auth-backend">
              <summary>Настройки сервера</summary>
              <label style="margin-top:10px">Backend URL
                <input v-model="baseUrl" class="input input--sm" placeholder="http://127.0.0.1:8000" />
              </label>
            </details>
            <button class="btn btn--primary btn--full" @click="login" :disabled="authLoading">
              <svg v-if="authLoading" class="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
              {{ authLoading ? 'Входим...' : 'Войти' }}
            </button>
            <p class="auth-switch">Нет аккаунта? <button class="link-btn" @click="authMode = 'register'">Зарегистрироваться</button></p>
            <p v-if="authError" class="error-msg">{{ authError }}</p>
          </div>

          <!-- REGISTER -->
          <div v-else class="auth-form">
            <h2>Регистрация</h2>
            <label>ФИО
              <input v-model="registerForm.full_name" class="input" placeholder="Иванов Иван Иванович" />
            </label>
            <label>Email
              <input v-model="registerForm.email" class="input" type="email" placeholder="you@company.ru" />
            </label>
            <label>Телефон
              <input v-model="registerForm.phone" class="input" type="tel" placeholder="+7 900 000 00 00" />
            </label>
            <label>Пароль
              <input v-model="registerForm.password" class="input" type="password" placeholder="••••••••" />
            </label>
            <label>Роль
              <select v-model="registerForm.role" class="input">
                <option value="employee">Сотрудник</option>
                <option value="boss">Начальник</option>
                <option value="admin">Администратор</option>
              </select>
            </label>
            <details class="auth-backend">
              <summary>Настройки сервера</summary>
              <label style="margin-top:10px">Backend URL
                <input v-model="baseUrl" class="input input--sm" placeholder="http://127.0.0.1:8000" />
              </label>
            </details>
            <button class="btn btn--primary btn--full" @click="registerUser" :disabled="authLoading">
              {{ authLoading ? 'Регистрируемся...' : 'Зарегистрироваться' }}
            </button>
            <p class="auth-switch">Уже есть аккаунт? <button class="link-btn" @click="authMode = 'login'">Войти</button></p>
            <p v-if="authError" class="error-msg">{{ authError }}</p>
          </div>
        </div>
      </div>
    </transition>

    <!-- ===== ОСНОВНОЕ ПРИЛОЖЕНИЕ ===== -->
    <div v-if="token" class="app-layout">

      <!-- HEADER -->
      <header class="header">
        <div class="header__left">
          <svg width="30" height="30" viewBox="0 0 44 44" fill="none">
            <rect width="44" height="44" rx="10" fill="#1a7fc4"/>
            <path d="M10 34V10h18l-6 8h-6v16H10z" fill="white"/>
            <path d="M22 10h12l-6 8H22l6-8z" fill="white" opacity="0.6"/>
          </svg>
          <span class="header__brand">Флагман</span>
        </div>

        <nav class="header__tabs" v-if="userRole" role="tablist">
          <button
            v-for="tab in visibleTabs"
            :key="tab.key"
            class="header__tab"
            :class="{ active: activeTab === tab.key }"
            role="tab"
            :aria-selected="activeTab === tab.key"
            @click="switchTab(tab.key)"
          >
            {{ tab.label }}
            <span v-if="tab.badge && newCount > 0" class="badge">{{ newCount }}</span>
          </button>
        </nav>

        <div class="header__right">
          <!-- Роль — только читаемый текст, без возможности менять -->
          <div class="role-pill" title="Ваша роль в системе">
            <span class="role-icon" aria-hidden="true">{{ roleIcon }}</span>
            <span class="role-label">{{ roleLabel }}</span>
          </div>
          <span class="user-name">{{ currentUser?.full_name ?? currentUser?.email ?? 'Пользователь' }}</span>
          <button class="btn btn--ghost btn--sm" @click="logout">Выйти</button>
          <button class="icon-btn" @click="toggleTheme" :aria-label="theme === 'light' ? 'Тёмная тема' : 'Светлая тема'">
            <svg v-if="theme === 'light'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          </button>
        </div>
      </header>

      <!-- TOAST уведомление -->
      <transition name="slide-down">
        <div v-if="toast.visible" class="toast" :class="'toast--' + toast.type" role="alert">
          {{ toast.message }}
          <button class="toast__close" @click="toast.visible = false">✕</button>
        </div>
      </transition>

      <!-- КОНТЕНТ -->
      <main class="page" role="main">
        <transition name="tab-fade" mode="out-in">

          <!-- ======== ГЛАВНАЯ ======== -->
          <section v-if="activeTab === 'home'" key="home">
            <div class="page-header">
              <div>
                <h1>Добро пожаловать{{ currentUser?.full_name ? ', ' + firstName : '' }}</h1>
                <p class="page-sub">{{ roleDescription }}</p>
              </div>
            </div>

            <div class="kpi-row">
              <div class="kpi-card" @click="switchTab('inbox')" style="cursor:pointer">
                <span class="kpi-label">Входящих</span>
                <span class="kpi-value">{{ inboxList.length }}</span>
                <span class="kpi-sub">всего получено</span>
              </div>
              <div class="kpi-card" @click="switchTab('read_unsigned')" style="cursor:pointer">
                <span class="kpi-label">Ожидают подписи</span>
                <span class="kpi-value kpi-value--warn">{{ pendingList.length }}</span>
                <span class="kpi-sub">нужно подписать</span>
              </div>
              <div class="kpi-card" @click="switchTab('signed')" style="cursor:pointer">
                <span class="kpi-label">Подписанных</span>
                <span class="kpi-value kpi-value--ok">{{ outboxList.length }}</span>
                <span class="kpi-sub">завершено</span>
              </div>
              <div v-if="userRole === 'admin'" class="kpi-card">
                <span class="kpi-label">Система</span>
                <span class="kpi-value kpi-value--ok" style="font-size:14px;font-weight:700">● Онлайн</span>
                <span class="kpi-sub">{{ baseUrl }}</span>
              </div>
            </div>

            <!-- ADMIN: управление структурой -->
            <template v-if="userRole === 'admin'">
              <div class="section-block">
                <h2 class="section-title">Управление структурой</h2>
                <div class="cards-grid">
                  <div class="card">
                    <div class="card__title">🏢 Организация</div>
                    <div class="form-col">
                      <label class="field-label">Название
                        <input v-model="organizationForm.name" class="input" placeholder="ООО Ромашка" />
                      </label>
                      <button class="btn btn--primary" @click="createOrganization">Создать</button>
                    </div>
                    <p class="hint" v-if="lastIds.organization_id">ID: <code>{{ lastIds.organization_id }}</code></p>
                  </div>
                  <div class="card">
                    <div class="card__title">🗂 Отдел</div>
                    <div class="form-col">
                      <label class="field-label">ID организации
                        <input v-model.number="departmentForm.organization_id" class="input" type="number" placeholder="1" />
                      </label>
                      <label class="field-label">Название отдела
                        <input v-model="departmentForm.name" class="input" placeholder="Бухгалтерия" />
                      </label>
                      <button class="btn btn--primary" @click="createDepartment">Создать отдел</button>
                    </div>
                    <p class="hint" v-if="lastIds.department_id">ID: <code>{{ lastIds.department_id }}</code></p>
                  </div>
                  <div class="card">
                    <div class="card__title">👤 Пригласить сотрудника</div>
                    <div class="form-col">
                      <label class="field-label">ID пользователя
                        <input v-model.number="inviteForm.user_id" class="input" type="number" placeholder="2" />
                      </label>
                      <label class="field-label">ID организации
                        <input v-model.number="inviteForm.organization_id" class="input" type="number" placeholder="1" />
                      </label>
                      <button class="btn btn--primary" @click="inviteEmployee">Пригласить</button>
                    </div>
                  </div>
                  <div class="card">
                    <div class="card__title">🔑 Выдать роль</div>
                    <div class="form-col">
                      <label class="field-label">ID пользователя
                        <input v-model.number="roleForm.user_id" class="input" type="number" placeholder="2" />
                      </label>
                      <label class="field-label">ID организации
                        <input v-model.number="roleForm.organization_id" class="input" type="number" placeholder="1" />
                      </label>
                      <label class="field-label">ID отдела
                        <input v-model.number="roleForm.department_id" class="input" type="number" placeholder="1" />
                      </label>
                      <label class="field-label">Название роли
                        <input v-model="roleForm.role_name" class="input" placeholder="sender / signer" />
                      </label>
                      <div class="checks-row">
                        <label class="check-label"><input type="checkbox" v-model="roleForm.can_send_document" /><span>Отправка</span></label>
                        <label class="check-label"><input type="checkbox" v-model="roleForm.can_sign_document" /><span>Подпись</span></label>
                        <label class="check-label"><input type="checkbox" v-model="roleForm.can_manage_department" /><span>Управление</span></label>
                      </div>
                      <div class="btn-row">
                        <button class="btn btn--ghost btn--sm" @click="setSenderRole">Шаблон: Начальник</button>
                        <button class="btn btn--ghost btn--sm" @click="setSignerRole">Шаблон: Сотрудник</button>
                      </div>
                      <button class="btn btn--primary" @click="assignRole">Выдать роль</button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="section-block">
                <h2 class="section-title">Настройки сервера</h2>
                <div class="card card--narrow">
                  <label class="field-label">Backend URL
                    <input v-model="baseUrl" class="input" placeholder="http://127.0.0.1:8000" />
                  </label>
                  <div class="ids-list">
                    <span>user_id: <code>{{ lastIds.user_id ?? '—' }}</code></span>
                    <span>org: <code>{{ lastIds.organization_id ?? '—' }}</code></span>
                    <span>dept: <code>{{ lastIds.department_id ?? '—' }}</code></span>
                    <span>doc: <code>{{ lastIds.document_id ?? '—' }}</code></span>
                  </div>
                </div>
              </div>
            </template>

            <!-- BOSS: единая форма создать и отправить -->
            <div v-if="userRole === 'boss'" class="section-block">
              <h2 class="section-title">Создать и отправить документ</h2>
              <div class="card card--form-center">
                <div class="card__title">📄 Новый документ</div>
                <div class="form-col">
                  <label class="field-label">Заголовок
                    <input v-model="documentForm.title" class="input" placeholder="Приказ №12" />
                  </label>
                  <label class="field-label">Содержимое
                    <textarea v-model="documentForm.content" class="input textarea" placeholder="Текст документа..." rows="4"></textarea>
                  </label>
                  <label class="field-label">Ссылка (необязательно)
                    <input v-model="documentForm.link" class="input" placeholder="https://..." />
                  </label>
                  <div class="form-row">
                    <label class="field-label" style="flex:1">Организация
                      <select v-model.number="documentForm.organization_id" class="input">
                        <option :value="null" disabled>— выберите —</option>
                        <option v-for="org in organizations" :key="org.id" :value="org.id">{{ org.name }}</option>
                      </select>
                    </label>
                    <label class="field-label" style="flex:1">Отдел
                      <select v-model.number="documentForm.department_id" class="input">
                        <option :value="null" disabled>— выберите —</option>
                        <option v-for="dep in departments" :key="dep.id" :value="dep.id">{{ dep.name }}</option>
                      </select>
                    </label>
                  </div>
                  <div class="form-row">
                    <label class="field-label" style="flex:1">Получатель
                      <select v-model.number="sendForm.recipient_user_id" class="input">
                        <option :value="null" disabled>— выберите —</option>
                        <option v-for="emp in employees" :key="emp.user_id" :value="emp.user_id">{{ emp.full_name ?? emp.email }}</option>
                      </select>
                    </label>
                  </div>
                  <button class="btn btn--primary" @click="createAndSend">Создать и отправить</button>
                </div>
              </div>
            </div>

            <!-- EMPLOYEE: требуют подписи -->
            <div v-if="userRole === 'employee'" class="section-block">
              <div class="section-title-row">
                <h2 class="section-title">Требуют вашей подписи</h2>
                <button class="btn btn--ghost btn--sm" @click="loadPending">Обновить</button>
              </div>
              <div v-if="pendingList.length" class="doc-list">
                <div v-for="doc in pendingList" :key="doc.document_id" class="doc-row doc-row--pending">
                  <div class="doc-row__info">
                    <span class="doc-title">{{ doc.title ?? 'Документ #' + doc.document_id }}</span>
                    <span class="doc-id">ID: {{ doc.document_id }}</span>
                  </div>
                  <div class="doc-row__actions">
                    <span class="doc-status doc-status--pending">На подписи</span>
                    <button class="btn btn--primary btn--sm" @click="quickSign(doc.document_id)">Подписать</button>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.35"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                <p>Все документы подписаны — отлично!</p>
              </div>
            </div>
          </section>

          <!-- ======== ПОЛУЧЕННЫЕ ПИСЬМА ======== -->
          <section v-else-if="activeTab === 'inbox'" key="inbox">
            <div class="page-header">
              <div>
                <h1>Полученные письма</h1>
                <p class="page-sub">Все входящие документы</p>
              </div>
              <button class="btn btn--ghost btn--sm" @click="loadInbox">↻ Обновить</button>
            </div>
            <div class="filter-bar">
              <label class="field-label">ID пользователя
                <input v-model.number="inboxUserId" class="input input--sm" type="number" placeholder="ID" />
              </label>
              <button class="btn btn--primary btn--sm" @click="loadInbox">Загрузить</button>
              <button class="btn btn--ghost btn--sm" @click="inboxUserId = lastIds.user_id">Мой ID</button>
            </div>
            <div v-if="inboxList.length" class="doc-list">
              <div
                v-for="doc in inboxList"
                :key="doc.document_id ?? doc.id"
                class="doc-row"
                :class="{ 'doc-row--new': doc.status === 'new' || !doc.status, 'doc-row--pending': doc.status === 'pending', 'doc-row--signed': doc.status === 'signed' }"
              >
                <div class="doc-row__info">
                  <span class="doc-title">{{ doc.title ?? 'Документ #' + (doc.document_id ?? doc.id) }}</span>
                  <span class="doc-id">ID: {{ doc.document_id ?? doc.id }}</span>
                </div>
                <span
                  class="doc-status"
                  :class="{ 'doc-status--new': doc.status === 'new' || !doc.status, 'doc-status--pending': doc.status === 'pending', 'doc-status--signed': doc.status === 'signed' }"
                >{{ docStatusLabel(doc.status) }}</span>
              </div>
            </div>
            <div v-else class="empty-state">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.35"><path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              <p>Нет входящих документов</p>
              <button class="btn btn--ghost btn--sm" @click="loadInbox">Загрузить</button>
            </div>
          </section>

          <!-- ======== ПРОЧИТАННЫЕ, НЕ ПОДПИСАННЫЕ ======== -->
          <section v-else-if="activeTab === 'read_unsigned'" key="read_unsigned">
            <div class="page-header">
              <div>
                <h1>Не подписанные</h1>
                <p class="page-sub">Документы, ожидающие вашей подписи</p>
              </div>
              <button class="btn btn--ghost btn--sm" @click="loadPending">↻ Обновить</button>
            </div>
            <div class="filter-bar">
              <label class="field-label">ID пользователя
                <input v-model.number="pendingUserId" class="input input--sm" type="number" placeholder="ID" />
              </label>
              <button class="btn btn--primary btn--sm" @click="loadPending">Загрузить</button>
              <button class="btn btn--ghost btn--sm" @click="pendingUserId = lastIds.user_id">Мой ID</button>
            </div>
            <div v-if="pendingList.length" class="doc-list">
              <div v-for="doc in pendingList" :key="doc.document_id" class="doc-row doc-row--pending">
                <div class="doc-row__info">
                  <span class="doc-title">{{ doc.title ?? 'Документ #' + doc.document_id }}</span>
                  <span class="doc-id">ID: {{ doc.document_id }}</span>
                </div>
                <div class="doc-row__actions">
                  <span class="doc-status doc-status--pending">Ожидает подписи</span>
                  <button class="btn btn--primary btn--sm" @click="quickSign(doc.document_id)">Подписать</button>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.35"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
              <p>Нет документов, ожидающих подписи</p>
            </div>
          </section>

          <!-- ======== ПОДПИСАННЫЕ ======== -->
          <section v-else-if="activeTab === 'signed'" key="signed">
            <div class="page-header">
              <div>
                <h1>Подписанные документы</h1>
                <p class="page-sub">Документы с завершённым статусом</p>
              </div>
              <button class="btn btn--ghost btn--sm" @click="loadOutbox">↻ Обновить</button>
            </div>
            <div class="filter-bar">
              <label class="field-label">ID пользователя
                <input v-model.number="outboxUserId" class="input input--sm" type="number" placeholder="ID" />
              </label>
              <button class="btn btn--primary btn--sm" @click="loadOutbox">Загрузить</button>
              <button class="btn btn--ghost btn--sm" @click="outboxUserId = lastIds.user_id">Мой ID</button>
            </div>
            <div v-if="outboxList.length" class="doc-list">
              <div v-for="doc in outboxList" :key="doc.document_id ?? doc.id" class="doc-row doc-row--signed">
                <div class="doc-row__info">
                  <span class="doc-title">{{ doc.title ?? 'Документ #' + (doc.document_id ?? doc.id) }}</span>
                  <span class="doc-id">ID: {{ doc.document_id ?? doc.id }}</span>
                </div>
                <span class="doc-status doc-status--signed">✓ Подписан</span>
              </div>
            </div>
            <div v-else class="empty-state">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.35"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              <p>Нет подписанных документов</p>
            </div>
          </section>

          <!-- ======== СОТРУДНИК: ПОДПИСАТЬ ======== -->
          <section v-else-if="activeTab === 'sign'" key="sign">
            <div class="page-header">
              <div>
                <h1>Подписать документ</h1>
                <p class="page-sub">Подписание на основе номера телефона</p>
              </div>
            </div>
            <div class="card card--narrow">
              <div class="card__title">Введите ID документа</div>
              <div class="form-col">
                <label class="field-label">ID документа
                  <input v-model.number="signForm.document_id" class="input" type="number" placeholder="1" />
                </label>
                <button class="btn btn--ghost btn--sm" @click="signForm.document_id = lastIds.document_id">Подставить последний ID</button>
                <button class="btn btn--primary" @click="signDocument">Подписать документ</button>
              </div>
            </div>
          </section>

          <!-- ======== АДМИНИСТРАТОР: ИНФОРМАЦИЯ ======== -->
          <section v-else-if="activeTab === 'admin_info'" key="admin_info">
            <div class="page-header">
              <div>
                <h1>Информация по системе</h1>
                <p class="page-sub">Полный мониторинг документов и статусов</p>
              </div>
            </div>
            <div class="cards-grid">
              <div class="card">
                <div class="card__title">🔍 Статус документа</div>
                <div class="form-col">
                  <label class="field-label">ID документа
                    <input v-model.number="statusForm.document_id" class="input" type="number" placeholder="1" />
                  </label>
                  <label class="field-label">ID получателя
                    <input v-model.number="statusForm.recipient_user_id" class="input" type="number" placeholder="2" />
                  </label>
                  <button class="btn btn--ghost btn--sm" @click="fillStatusIds">Подставить ID</button>
                  <button class="btn btn--primary" @click="loadStatus">Проверить статус</button>
                </div>
                <div v-if="statusResult" class="json-preview" style="margin-top:12px">
                  <pre>{{ pretty(statusResult) }}</pre>
                </div>
              </div>
              <div class="card">
                <div class="card__title">📡 Последний ответ сервера</div>
                <div class="json-preview">
                  <pre>{{ pretty(output) }}</pre>
                </div>
                <button class="btn btn--ghost btn--sm" style="margin-top:10px" @click="clearOutput">Очистить</button>
              </div>
            </div>
          </section>

        </transition>
      </main>

      <!-- STATUS BAR (только для admin) -->
      <transition name="slide-up">
        <div v-if="output && userRole === 'admin'" class="status-bar">
          <span class="status-bar__label">Ответ:</span>
          <code class="status-bar__code">{{ shortOutput }}</code>
          <button class="status-bar__close" @click="clearOutput" aria-label="Закрыть">✕</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

// ---- STATE ----
const baseUrl      = ref('http://127.0.0.1:8000')
const activeTab    = ref('home')
const token        = ref(null)
const currentUser  = ref(null)
const authMode     = ref('login')
const authLoading  = ref(false)
const authError    = ref('')
const theme        = ref('light')
const userRole     = ref(null)   // берётся только с бэкенда через /auth/me
const output       = ref(null)
const inboxList    = ref([])
const outboxList   = ref([])
const pendingList  = ref([])
const statusResult = ref(null)
const inboxUserId  = ref(null)
const outboxUserId = ref(null)
const pendingUserId = ref(null)
const organizations = ref([])
const departments   = ref([])
const employees     = ref([])

const toast = reactive({ visible: false, message: '', type: 'success' })

const lastIds = reactive({
  user_id: null, organization_id: null,
  department_id: null, document_id: null, recipient_user_id: null
})

const registerForm = reactive({ full_name: '', email: '', phone: '', password: '', role: 'employee' })
const loginForm    = reactive({ email: '', password: '' })
const organizationForm = reactive({ name: '' })
const departmentForm   = reactive({ organization_id: null, name: '' })
const inviteForm       = reactive({ user_id: null, organization_id: null })
const roleForm         = reactive({
  user_id: null, organization_id: null, department_id: null,
  role_name: '', can_send_document: false, can_sign_document: false, can_manage_department: false
})
const documentForm = reactive({ title: '', content: '', link: '', organization_id: null, department_id: null })
const sendForm     = reactive({ document_id: null, organization_id: null, department_id: null, recipient_user_id: null })
const signForm     = reactive({ document_id: null })
const statusForm   = reactive({ document_id: null, recipient_user_id: null })

// ---- COMPUTED ----
const roleIcon = computed(() => ({ admin: '🛡️', boss: '👔', employee: '👤' }[userRole.value] || '👤'))

const roleLabel = computed(() => ({ admin: 'Администратор', boss: 'Начальник', employee: 'Сотрудник' }[userRole.value] || userRole.value || ''))

const firstName = computed(() => {
  const name = currentUser.value?.full_name ?? ''
  return name.split(' ')[0] || ''
})

const roleDescription = computed(() => ({
  admin:    'Администратор — полный контроль над системой',
  boss:     'Начальник — создание и отправка документов на подпись',
  employee: 'Сотрудник — просмотр и подписание входящих документов'
})[userRole.value] || '')

const newCount = computed(() => inboxList.value.filter(d => d.status === 'new' || !d.status).length)

const visibleTabs = computed(() => {
  const common = [
    { key: 'home',          label: 'Главная' },
    { key: 'inbox',         label: 'Полученные письма', badge: true },
    { key: 'read_unsigned', label: 'Не подписанные' },
    { key: 'signed',        label: 'Подписанные' },
  ]
  if (userRole.value === 'boss')     return common
  if (userRole.value === 'employee') return [...common, { key: 'sign', label: 'Подписать' }]
  if (userRole.value === 'admin')    return [...common, { key: 'admin_info', label: 'Мониторинг' }]
  return common
})

const shortOutput = computed(() => {
  if (!output.value) return '—'
  const s = JSON.stringify(output.value)
  return s.length > 140 ? s.slice(0, 140) + '…' : s
})

// ---- HELPERS ----
function docStatusLabel(status) {
  return ({ new: 'Новое', pending: 'На подписи', signed: 'Подписан', read: 'Прочитано' }[status] || 'Новое')
}

function toggleTheme() { theme.value = theme.value === 'light' ? 'dark' : 'light' }
function pretty(v)     { return (v == null) ? 'Нет данных' : JSON.stringify(v, null, 2) }
function clearOutput() { output.value = null }
function logout()      { token.value = null; currentUser.value = null; userRole.value = null; authMode.value = 'login'; authError.value = '' }

function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.visible = true
  setTimeout(() => { toast.visible = false }, 3500)
}

function switchTab(key) {
  activeTab.value = key
  if (key === 'inbox')         loadInbox()
  if (key === 'read_unsigned') loadPending()
  if (key === 'signed')        loadOutbox()
}

function normalizeError(data) {
  if (!data) return 'Неизвестная ошибка'
  if (typeof data === 'string') return data
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) return data.detail.map(i => `${(i.loc||[]).join(' → ')}: ${i.msg}`).join('\n')
  return JSON.stringify(data, null, 2)
}

function updateLastIds(data) {
  if (!data || typeof data !== 'object') return
  if ('id' in data && ('email' in data || 'full_name' in data)) lastIds.user_id = data.id
  if ('id' in data && 'name' in data && departmentForm.name === data.name) lastIds.department_id = data.id
  if ('department_id' in data) lastIds.department_id = data.department_id
  if ('id' in data && 'title' in data && 'content' in data) lastIds.document_id = data.id
  if ('recipient_user_id' in data) lastIds.recipient_user_id = data.recipient_user_id
}

function fillStatusIds() { statusForm.document_id = lastIds.document_id; statusForm.recipient_user_id = lastIds.recipient_user_id ?? lastIds.user_id }
function setSenderRole() { roleForm.role_name = 'sender';  roleForm.can_send_document = true;  roleForm.can_sign_document = false; roleForm.can_manage_department = false }
function setSignerRole() { roleForm.role_name = 'signer';  roleForm.can_send_document = false; roleForm.can_sign_document = true;  roleForm.can_manage_department = false }

// ---- API ----
async function apiRequest(path, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' }
  if (token.value) headers['Authorization'] = `Bearer ${token.value}`
  const options = { method, headers }
  if (body) options.body = JSON.stringify(body)
  const response = await fetch(`${baseUrl.value}${path}`, options)
  let data
  try { data = await response.json() } catch { data = { detail: 'Сервер вернул не JSON' } }
  if (!response.ok) {
    const message = normalizeError(data)
    output.value = { status: response.status, error: message, raw: data }
    throw new Error(message)
  }
  output.value = data
  updateLastIds(data)
  return data
}

async function registerUser() {
  authLoading.value = true; authError.value = ''
  try {
    const data = await apiRequest('/auth/register', 'POST', registerForm)
    if (data?.id) { lastIds.user_id = data.id; loginForm.email = registerForm.email; loginForm.password = registerForm.password; authMode.value = 'login' }
    showToast('Регистрация успешна! Войдите в систему.')
  } catch(e) { authError.value = e.message } finally { authLoading.value = false }
}

async function login() {
  authLoading.value = true; authError.value = ''
  try {
    const data = await apiRequest('/auth/login', 'POST', loginForm)
    if (data?.access_token) {
      token.value = data.access_token
      const me = await apiRequest('/auth/me', 'GET')
      currentUser.value = me
      // Роль берётся исключительно с бэкенда — пользователь не может её менять
      userRole.value = me.role
      lastIds.user_id = me.id
      inboxUserId.value = me.id; outboxUserId.value = me.id; pendingUserId.value = me.id
      activeTab.value = 'home'
      loadInbox(); loadPending(); loadOutbox()
      loadOrganizations()
    }
  } catch(e) { authError.value = e.message } finally { authLoading.value = false }
}

async function loadOrganizations() {
  try { const d = await apiRequest('/organizations/list'); organizations.value = Array.isArray(d) ? d : [] } catch { organizations.value = [] }
}

async function loadDepartmentsByOrg(orgId) {
  if (!orgId) return
  try { const d = await apiRequest(`/departments/list/${orgId}`); departments.value = Array.isArray(d) ? d : [] } catch { departments.value = [] }
}

async function loadEmployeesByDept(deptId) {
  if (!deptId) return
  try { const d = await apiRequest(`/employees/list/${deptId}`); employees.value = Array.isArray(d) ? d : [] } catch { employees.value = [] }
}

import { watch } from 'vue'
// immediate:true — если documentForm уже заполнен (например после createOrganization),
// watch сработает сразу при маунте, а не только при изменении значения
watch(() => documentForm.organization_id, (orgId) => { loadDepartmentsByOrg(orgId) }, { immediate: true })
watch(() => documentForm.department_id,   (deptId) => { loadEmployeesByDept(deptId) }, { immediate: true })

async function createAndSend() {
  try {
    const doc = await apiRequest('/documents/create', 'POST', {
      title: documentForm.title,
      content: documentForm.content,
      link: documentForm.link || undefined,
      organization_id: documentForm.organization_id,
      department_id: documentForm.department_id
    })
    if (!doc?.id) throw new Error('Документ не создан')
    await apiRequest('/documents/send', 'POST', {
      document_id: doc.id,
      organization_id: documentForm.organization_id,
      department_id: documentForm.department_id,
      recipient_user_id: sendForm.recipient_user_id
    })
    showToast('Документ создан и отправлен!')
    documentForm.title = ''; documentForm.content = ''; documentForm.link = ''
  } catch(e) { showToast(e.message, 'error') }
}

async function createOrganization() {
  try {
    const data = await apiRequest('/organizations/create', 'POST', organizationForm)
    if (data?.id) { lastIds.organization_id = data.id; departmentForm.organization_id = data.id; inviteForm.organization_id = data.id; roleForm.organization_id = data.id; documentForm.organization_id = data.id; sendForm.organization_id = data.id }
    showToast('Организация создана!')
    loadOrganizations()
  } catch(e) { showToast(e.message, 'error') }
}

async function createDepartment() {
  try {
    const data = await apiRequest('/departments/create', 'POST', departmentForm)
    if (data?.id) { lastIds.department_id = data.id; roleForm.department_id = data.id; documentForm.department_id = data.id; sendForm.department_id = data.id }
    showToast('Отдел создан!')
  } catch(e) { showToast(e.message, 'error') }
}

async function inviteEmployee() {
  try { await apiRequest('/employees/invite', 'POST', inviteForm); showToast('Сотрудник приглашён!') }
  catch(e) { showToast(e.message, 'error') }
}

async function assignRole() {
  try { await apiRequest('/access/assign-role', 'POST', roleForm); showToast('Роль выдана!') }
  catch(e) { showToast(e.message, 'error') }
}

async function signDocument() {
  try { await apiRequest('/signatures/sign', 'POST', signForm); loadPending(); showToast('Документ подписан!') }
  catch(e) { showToast(e.message, 'error') }
}

async function quickSign(docId) { signForm.document_id = docId; await signDocument() }

async function loadInbox() {
  const uid = inboxUserId.value ?? lastIds.user_id
  if (!uid) return
  try { const d = await apiRequest(`/documents/inbox/${uid}`); inboxList.value = Array.isArray(d) ? d : [] }
  catch { inboxList.value = [] }
}

async function loadOutbox() {
  const uid = outboxUserId.value ?? lastIds.user_id
  if (!uid) return
  try { const d = await apiRequest(`/documents/outbox/${uid}`); outboxList.value = Array.isArray(d) ? d : [] }
  catch { outboxList.value = [] }
}

async function loadPending() {
  const uid = pendingUserId.value ?? lastIds.user_id
  if (!uid) return
  try { const d = await apiRequest(`/documents/pending/${uid}`); pendingList.value = Array.isArray(d) ? d : [] }
  catch { pendingList.value = [] }
}

async function loadStatus() {
  try { statusResult.value = await apiRequest(`/documents/status/${statusForm.document_id}/${statusForm.recipient_user_id}`) }
  catch(e) { showToast(e.message, 'error') }
}
</script>

<style scoped>
.role-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

.field-label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
}

.section-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
.section-title-row .section-title { margin-bottom: 0; }

.kpi-sub {
  font-size: 11px;
  color: var(--text-faint);
  margin-top: 2px;
}

.form-row {
  display: flex;
  gap: 12px;
}

.card--form-center {
  max-width: 560px;
  margin: 0 auto;
}

.toast {
  position: fixed;
  top: calc(var(--header-h) + 12px);
  right: 20px;
  z-index: 300;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  font-size: 13px;
  font-weight: 600;
  box-shadow: var(--shadow-lg);
  max-width: 360px;
  border: 1px solid transparent;
}
.toast--success {
  background: var(--success-tint);
  color: var(--success);
  border-color: rgba(30,138,82,0.2);
}
.toast--error {
  background: var(--error-tint);
  color: var(--error);
  border-color: rgba(181,39,58,0.2);
}
.toast__close {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  opacity: 0.6;
  padding: 0 2px;
  color: inherit;
  margin-left: auto;
}
.toast__close:hover { opacity: 1; }

.spinner {
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.tab-fade-enter-active, .tab-fade-leave-active { transition: opacity 0.18s ease, transform 0.18s ease; }
.tab-fade-enter-from { opacity: 0; transform: translateY(6px); }
.tab-fade-leave-to   { opacity: 0; transform: translateY(-4px); }

.slide-down-enter-active, .slide-down-leave-active { transition: all 0.22s ease; }
.slide-down-enter-from { opacity: 0; transform: translateY(-12px); }
.slide-down-leave-to   { opacity: 0; transform: translateY(-12px); }

.slide-up-enter-active, .slide-up-leave-active { transition: all 0.22s ease; }
.slide-up-enter-from { opacity: 0; transform: translateY(8px); }
.slide-up-leave-to   { opacity: 0; transform: translateY(8px); }
</style>
