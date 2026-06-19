<template>
  <div id="app" :data-theme="theme">

    <!-- ===== ЭКРАН ВХОДА ===== -->
    <transition name="fade">
      <div v-if="!token" class="auth-screen">
        <div class="auth-card">
          <div class="auth-logo">
            <svg width="42" height="42" viewBox="0 0 44 44" fill="none" aria-label="Флагман">
              <rect width="44" height="44" rx="12" fill="#1a7fc4"/>
              <path d="M10 34V10h18l-6 8h-6v16H10z" fill="white"/>
              <path d="M22 10h12l-6 8H22l6-8z" fill="white" opacity="0.6"/>
            </svg>
            <span class="auth-logo__text">Флагман</span>
          </div>
          <p class="auth-subtitle">Сервис рассылки и подписания документов</p>

          <div v-if="authMode === 'login'" class="auth-form">
            <h2>Войти в аккаунт</h2>
            <label class="field-label">Email
              <input v-model="loginForm.email" class="input" type="email" placeholder="you@company.ru" autocomplete="email" />
            </label>
            <label class="field-label">Пароль
              <input v-model="loginForm.password" class="input" type="password" placeholder="••••••••" autocomplete="current-password" />
            </label>
            <details class="auth-backend">
              <summary>Настройки сервера</summary>
              <label class="field-label" style="margin-top:10px">Backend URL
                <input v-model="baseUrl" class="input input--sm" placeholder="http://127.0.0.1:8000" />
              </label>
            </details>
            <button class="btn btn--primary btn--full" @click="login" :disabled="authLoading">
              <svg v-if="authLoading" class="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
              {{ authLoading ? 'Входим...' : 'Войти' }}
            </button>
            <p class="auth-switch">Нет аккаунта? <button class="link-btn" @click="authMode = 'register'">Зарегистрироваться</button></p>
            <p v-if="authError" class="error-msg">{{ authError }}</p>
          </div>

          <div v-else class="auth-form">
            <h2>Регистрация</h2>
            <label class="field-label">ФИО
              <input v-model="registerForm.full_name" class="input" placeholder="Иванов Иван Иванович" />
            </label>
            <label class="field-label">Email
              <input v-model="registerForm.email" class="input" type="email" placeholder="you@company.ru" />
            </label>
            <label class="field-label">Телефон
              <input v-model="registerForm.phone" class="input" type="tel" placeholder="+7 900 000 00 00" />
            </label>
            <label class="field-label">Пароль
              <input v-model="registerForm.password" class="input" type="password" placeholder="мин. 6 символов" />
            </label>
            <label class="field-label">Роль
              <select v-model="registerForm.role" class="input">
                <option value="employee">Сотрудник</option>
                <option value="boss">Начальник</option>
              </select>
            </label>
            <details class="auth-backend">
              <summary>Настройки сервера</summary>
              <label class="field-label" style="margin-top:10px">Backend URL
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

      <header class="header">
        <div class="header__left">
          <svg width="30" height="30" viewBox="0 0 44 44" fill="none">
            <rect width="44" height="44" rx="10" fill="#1a7fc4"/>
            <path d="M10 34V10h18l-6 8h-6v16H10z" fill="white"/>
            <path d="M22 10h12l-6 8H22l6-8z" fill="white" opacity="0.6"/>
          </svg>
          <span class="header__brand">Флагман</span>
        </div>

        <nav class="header__tabs" role="tablist">
          <button
            v-for="tab in visibleTabs" :key="tab.key"
            class="header__tab" :class="{ active: activeTab === tab.key }"
            role="tab" :aria-selected="activeTab === tab.key"
            @click="switchTab(tab.key)"
          >
            {{ tab.label }}
            <span v-if="tab.badge && newCount > 0" class="badge">{{ newCount }}</span>
          </button>
        </nav>

        <div class="header__right">
          <div class="role-pill" :class="'role-pill--' + userRole">
            <span>{{ roleIcon }}</span>
            <span>{{ roleLabel }}</span>
          </div>
          <span class="user-name">{{ currentUser?.full_name ?? '' }}</span>
          <button class="btn btn--ghost btn--sm" @click="logout">Выйти</button>
          <button class="icon-btn" @click="toggleTheme" :aria-label="theme === 'light' ? 'Тёмная' : 'Светлая'">
            <svg v-if="theme==='light'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          </button>
        </div>
      </header>

      <transition name="slide-down">
        <div v-if="toast.visible" class="toast" :class="'toast--' + toast.type" role="alert">
          {{ toast.message }}
          <button class="toast__close" @click="toast.visible = false">✕</button>
        </div>
      </transition>

      <main class="page" role="main">
        <transition name="tab-fade" mode="out-in">

          <!-- ======== ГЛАВНАЯ ======== -->
          <section v-if="activeTab === 'home'" key="home">
            <div class="page-header">
              <div>
                <h1>Добро пожаловать{{ firstName ? ', ' + firstName : '' }}</h1>
                <p class="page-sub">{{ roleDescription }}</p>
              </div>
            </div>
            <div class="kpi-row">
              <div class="kpi-card" @click="switchTab('inbox')" style="cursor:pointer">
                <span class="kpi-label">Входящих</span>
                <span class="kpi-value">{{ inboxList.length }}</span>
                <span class="kpi-sub">получено</span>
              </div>
              <div class="kpi-card" @click="switchTab('read_unsigned')" style="cursor:pointer">
                <span class="kpi-label">На подписи</span>
                <span class="kpi-value kpi-value--warn">{{ pendingList.length }}</span>
                <span class="kpi-sub">ждут действия</span>
              </div>
              <div class="kpi-card" @click="switchTab('signed')" style="cursor:pointer">
                <span class="kpi-label">Подписанных</span>
                <span class="kpi-value kpi-value--ok">{{ signedList.length }}</span>
                <span class="kpi-sub">завершено</span>
              </div>
              <div v-if="isAdmin" class="kpi-card">
                <span class="kpi-label">Пользователей</span>
                <span class="kpi-value">{{ allUsers.length }}</span>
                <span class="kpi-sub">в системе</span>
              </div>
            </div>

            <!-- ADMIN HOME -->
            <template v-if="isAdmin">
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
                      <button class="btn btn--ghost btn--sm" @click="loadOrganizations">↻ Загрузить список</button>
                    </div>
                    <div v-if="organizations.length" class="mini-list">
                      <div v-for="o in organizations" :key="o.id" class="mini-row">
                        <span class="mini-name">{{ o.name }}</span>
                        <span class="mini-id">ID: {{ o.id }}</span>
                        <button class="btn btn--ghost btn--xs" @click="deleteOrganization(o.id)">×</button>
                      </div>
                    </div>
                  </div>

                  <div class="card">
                    <div class="card__title">🗂 Отдел</div>
                    <div class="form-col">
                      <label class="field-label">Организация
                        <select v-model="departmentForm.organization_id" class="input" @change="loadDepartmentsByOrg(departmentForm.organization_id)">
                          <option :value="null" disabled>— выберите —</option>
                          <option v-for="o in organizations" :key="o.id" :value="o.id">{{ o.name }}</option>
                        </select>
                      </label>
                      <label class="field-label">Название отдела
                        <input v-model="departmentForm.name" class="input" placeholder="Бухгалтерия" />
                      </label>
                      <button class="btn btn--primary" @click="createDepartment">Создать отдел</button>
                    </div>
                    <div v-if="departments.length" class="mini-list">
                      <div v-for="d in departments" :key="d.id" class="mini-row">
                        <span class="mini-name">{{ d.name }}</span>
                        <span class="mini-id">ID: {{ d.id }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="card">
                    <div class="card__title">👤 Пригласить сотрудника</div>
                    <div class="form-col">
                      <label class="field-label">Пользователь
                        <select v-model="inviteForm.user_id" class="input">
                          <option :value="null" disabled>— выберите —</option>
                          <option v-for="u in allUsers" :key="u.id" :value="u.id">{{ u.full_name }} ({{ u.email }})</option>
                        </select>
                      </label>
                      <label class="field-label">Организация
                        <select v-model="inviteForm.organization_id" class="input">
                          <option :value="null" disabled>— выберите —</option>
                          <option v-for="o in organizations" :key="o.id" :value="o.id">{{ o.name }}</option>
                        </select>
                      </label>
                      <button class="btn btn--primary" @click="inviteEmployee">Пригласить</button>
                    </div>
                  </div>

                  <div class="card">
                    <div class="card__title">🔑 Выдать роль</div>
                    <div class="form-col">
                      <label class="field-label">Пользователь
                        <select v-model="roleForm.user_id" class="input">
                          <option :value="null" disabled>— выберите —</option>
                          <option v-for="u in allUsers" :key="u.id" :value="u.id">{{ u.full_name }} ({{ u.role }})</option>
                        </select>
                      </label>
                      <label class="field-label">Организация
                        <select v-model="roleForm.organization_id" class="input" @change="loadDepartmentsByOrg(roleForm.organization_id)">
                          <option :value="null" disabled>— выберите —</option>
                          <option v-for="o in organizations" :key="o.id" :value="o.id">{{ o.name }}</option>
                        </select>
                      </label>
                      <label class="field-label">Отдел
                        <select v-model="roleForm.department_id" class="input">
                          <option :value="null" disabled>— выберите —</option>
                          <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
                        </select>
                      </label>
                      <label class="field-label">Название роли
                        <input v-model="roleForm.role_name" class="input" placeholder="sender / signer" />
                      </label>
                      <div class="checks-row">
                        <label class="check-label"><input type="checkbox" v-model="roleForm.can_send_document"/><span>Отправка</span></label>
                        <label class="check-label"><input type="checkbox" v-model="roleForm.can_sign_document"/><span>Подпись</span></label>
                        <label class="check-label"><input type="checkbox" v-model="roleForm.can_manage_department"/><span>Управление</span></label>
                      </div>
                      <div class="btn-row">
                        <button class="btn btn--ghost btn--sm" @click="setSenderRole">Начальник</button>
                        <button class="btn btn--ghost btn--sm" @click="setSignerRole">Сотрудник</button>
                      </div>
                      <button class="btn btn--primary" @click="assignRole">Выдать роль</button>
                    </div>
                  </div>

                </div>
              </div>
            </template>

            <!-- BOSS HOME — единая форма создания и отправки -->
            <div v-if="isBoss" class="section-block">
              <h2 class="section-title">Новый документ</h2>
              <div class="card card--wide">
                <div class="form-col">
                  <label class="field-label">Заголовок
                    <input v-model="documentForm.title" class="input" placeholder="Приказ №12" />
                  </label>

                  <label class="field-label">Содержимое
                    <textarea v-model="documentForm.content" class="input textarea" placeholder="Текст документа..." rows="3"></textarea>
                  </label>

                  <label class="field-label">Ссылка <span class="field-optional">(необязательно)</span>
                    <input v-model="documentForm.link" class="input" type="url" placeholder="https://example.com/doc.pdf" />
                  </label>

                  <div class="form-row">
                    <label class="field-label" style="flex:1">Организация
                      <select v-model="documentForm.organization_id" class="input" @change="onDocOrgChange">
                        <option :value="null" disabled>— выберите —</option>
                        <option v-for="o in organizations" :key="o.id" :value="o.id">{{ o.name }}</option>
                      </select>
                      <span v-if="!organizations.length" class="hint-warn">⚠ Организаций нет. Попросите администратора.</span>
                    </label>
                    <label class="field-label" style="flex:1">Отдел
                      <select v-model="documentForm.department_id" class="input">
                        <option :value="null" disabled>— выберите —</option>
                        <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
                      </select>
                    </label>
                  </div>

                  <label class="field-label">Получатель
                    <select v-model="sendForm.recipient_user_id" class="input">
                      <option :value="null" disabled>— выберите —</option>
                      <option v-for="u in orgUsers" :key="u.id" :value="u.user_id ?? u.id">{{ u.full_name }} ({{ u.email }})</option>
                    </select>
                    <span v-if="usersLoading" class="hint">⏳ Загружаем сотрудников...</span>
                    <span v-else-if="documentForm.organization_id && !orgUsers.length" class="hint-warn">⚠ Нет сотрудников в этой организации</span>
                  </label>

                  <button
                    class="btn btn--primary"
                    @click="createAndSend"
                    :disabled="sendLoading || !documentForm.organization_id || !documentForm.department_id"
                  >
                    <svg v-if="sendLoading" class="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
                    {{ sendLoading ? 'Отправляем...' : 'Создать и отправить' }}
                  </button>

                  <p v-if="lastIds.document_id" class="hint success">✓ Последний документ ID: <code>{{ lastIds.document_id }}</code></p>
                </div>
              </div>
            </div>

            <!-- EMPLOYEE HOME -->
            <div v-if="isEmployee" class="section-block">
              <div class="section-title-row">
                <h2 class="section-title">Требуют вашей подписи</h2>
                <button class="btn btn--ghost btn--sm" @click="loadPending">↻</button>
              </div>
              <div v-if="pendingList.length" class="doc-list">
                <div v-for="doc in pendingList" :key="doc.document_id" class="doc-row doc-row--pending">
                  <div class="doc-row__info">
                    <span class="doc-title">{{ doc.title ?? 'Dok. #' + doc.document_id }}</span>
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
                <p>Все подписано!</p>
              </div>
            </div>
          </section>

          <!-- ======== ПОЛУЧЕННЫЕ ======== -->
          <section v-else-if="activeTab === 'inbox'" key="inbox">
            <div class="page-header">
              <div><h1>Полученные письма</h1><p class="page-sub">Все входящие документы</p></div>
              <button class="btn btn--ghost btn--sm" @click="loadInbox">↻ Обновить</button>
            </div>
            <div v-if="inboxList.length" class="doc-list">
              <div v-for="doc in inboxList" :key="doc.document_id" class="doc-row"
                :class="{ 'doc-row--new': !doc.status || doc.status==='new', 'doc-row--pending': doc.status==='pending', 'doc-row--signed': doc.status==='signed' }">
                <div class="doc-row__info">
                  <span class="doc-title">{{ doc.title ?? 'Dok. #' + doc.document_id }}</span>
                  <span class="doc-id">ID: {{ doc.document_id }} &middot; От польз. #{{ doc.sender_user_id }}</span>
                  <a v-if="doc.link" :href="doc.link" target="_blank" rel="noopener" class="doc-link">🔗 Открыть ссылку</a>
                </div>
                <div class="doc-row__actions">
                  <span class="doc-status" :class="statusClass(doc.status)">{{ docStatusLabel(doc.status) }}</span>
                  <button v-if="doc.status !== 'signed'" class="btn btn--primary btn--sm" @click="quickSign(doc.document_id)">Подписать</button>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.35"><path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              <p>Нет входящих документов</p>
            </div>
          </section>

          <!-- ======== НЕ ПОДПИСАННЫЕ ======== -->
          <section v-else-if="activeTab === 'read_unsigned'" key="read_unsigned">
            <div class="page-header">
              <div><h1>Не подписанные</h1><p class="page-sub">Ожидают подписи</p></div>
              <button class="btn btn--ghost btn--sm" @click="loadPending">↻ Обновить</button>
            </div>
            <div v-if="pendingList.length" class="doc-list">
              <div v-for="doc in pendingList" :key="doc.document_id" class="doc-row doc-row--pending">
                <div class="doc-row__info">
                  <span class="doc-title">{{ doc.title ?? 'Dok. #' + doc.document_id }}</span>
                  <span class="doc-id">ID: {{ doc.document_id }}</span>
                  <a v-if="doc.link" :href="doc.link" target="_blank" rel="noopener" class="doc-link">🔗 Открыть ссылку</a>
                </div>
                <div class="doc-row__actions">
                  <span class="doc-status doc-status--pending">Ожидает</span>
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
              <div><h1>Подписанные</h1><p class="page-sub">Документы, которые вы подписали</p></div>
              <button class="btn btn--ghost btn--sm" @click="loadSigned">↻ Обновить</button>
            </div>
            <div v-if="signedList.length" class="doc-list">
              <div v-for="doc in signedList" :key="doc.document_id" class="doc-row doc-row--signed">
                <div class="doc-row__info">
                  <span class="doc-title">{{ doc.title ?? 'Dok. #' + doc.document_id }}</span>
                  <span class="doc-id">ID: {{ doc.document_id }} &middot; От польз. #{{ doc.sender_user_id }}</span>
                  <a v-if="doc.link" :href="doc.link" target="_blank" rel="noopener" class="doc-link">🔗 Открыть ссылку</a>
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
          <section v-else-if="activeTab === 'sign' && isEmployee" key="sign">
            <div class="page-header">
              <div><h1>Подписать документ</h1></div>
            </div>
            <div class="card card--narrow">
              <div class="form-col">
                <label class="field-label">ID документа
                  <input v-model.number="signForm.document_id" class="input" type="number" placeholder="1" />
                </label>
                <button class="btn btn--ghost btn--sm" @click="signForm.document_id = lastIds.document_id">Подставить последний ID</button>
                <button class="btn btn--primary" @click="signDocument">Подписать</button>
              </div>
            </div>
          </section>

          <!-- ======== АДМИН: МОНИТОРИНГ ======== -->
          <section v-else-if="activeTab === 'admin_info' && isAdmin" key="admin_info">
            <div class="page-header">
              <div><h1>Мониторинг</h1><p class="page-sub">Полный контроль системы</p></div>
              <button class="btn btn--ghost btn--sm" @click="loadAllUsers">↻ Пользователи</button>
            </div>
            <div class="cards-grid">

              <div class="card">
                <div class="card__title">👥 Пользователи системы</div>
                <div v-if="allUsers.length" class="doc-list">
                  <div v-for="u in allUsers" :key="u.id" class="doc-row">
                    <div class="doc-row__info">
                      <span class="doc-title">{{ u.full_name }}</span>
                      <span class="doc-id">{{ u.email }} &middot; ID: {{ u.id }}</span>
                    </div>
                    <span class="doc-status" :class="{ 'doc-status--signed': u.role==='admin', 'doc-status--pending': u.role==='boss', 'doc-status--new': u.role==='employee' }">
                      {{ {admin:'🛡 Админ', boss:'👔 Начальник', employee:'👤 Сотрудник'}[u.role] ?? u.role }}
                    </span>
                  </div>
                </div>
                <p v-else class="hint">Нажмите «Обновить»</p>
              </div>

              <div class="card">
                <div class="card__title">🏢 Организации</div>
                <button class="btn btn--ghost btn--sm" style="margin-bottom:10px" @click="loadOrganizations">↻ Загрузить</button>
                <div class="doc-list">
                  <div v-for="o in organizations" :key="o.id" class="doc-row">
                    <div class="doc-row__info">
                      <span class="doc-title">{{ o.name }}</span>
                      <span class="doc-id">ID: {{ o.id }}</span>
                    </div>
                    <button class="btn btn--ghost btn--xs" @click="deleteOrganization(o.id)">× Удалить</button>
                  </div>
                </div>
                <div v-if="!organizations.length" class="empty-state" style="padding:12px 0">
                  <p style="font-size:13px">Организаций нет</p>
                </div>
              </div>

              <div class="card">
                <div class="card__title">🔍 Статус документа</div>
                <div class="form-col">
                  <label class="field-label">ID документа
                    <input v-model.number="statusForm.document_id" class="input" type="number" placeholder="1" />
                  </label>
                  <label class="field-label">ID получателя
                    <input v-model.number="statusForm.recipient_user_id" class="input" type="number" placeholder="2" />
                  </label>
                  <button class="btn btn--primary" @click="loadStatus">Проверить</button>
                </div>
                <div v-if="statusResult" class="json-preview" style="margin-top:10px"><pre>{{ pretty(statusResult) }}</pre></div>
              </div>

              <div class="card">
                <div class="card__title">📡 Последний ответ API</div>
                <div class="json-preview"><pre>{{ pretty(output) }}</pre></div>
                <button class="btn btn--ghost btn--sm" style="margin-top:8px" @click="clearOutput">Очистить</button>
              </div>

            </div>
          </section>

          <!-- ДОСТУП ЗАПРЕЩЁН -->
          <section v-else key="forbidden">
            <div class="empty-state" style="padding-top:80px">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><circle cx="12" cy="12" r="10"/><path d="M4.93 4.93l14.14 14.14"/></svg>
              <p style="margin-top:10px;font-size:15px">Доступ запрещён</p>
              <button class="btn btn--ghost btn--sm" style="margin-top:16px" @click="switchTab('home')">← На главную</button>
            </div>
          </section>

        </transition>
      </main>

      <transition name="slide-up">
        <div v-if="output && isAdmin" class="status-bar">
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

const baseUrl     = ref('http://127.0.0.1:8000')
const activeTab   = ref('home')
const token       = ref(null)
const currentUser = ref(null)
const userRole    = ref('')
const authMode    = ref('login')
const authLoading = ref(false)
const authError   = ref('')
const theme       = ref('light')
const output      = ref(null)
const inboxList   = ref([])
const outboxList  = ref([])
const signedList  = ref([])
const pendingList = ref([])
const allUsers    = ref([])
const orgUsers    = ref([])
const usersLoading = ref(false)
const sendLoading  = ref(false)
const organizations = ref([])
const departments   = ref([])
const statusResult  = ref(null)
const sentDocuments = ref([])

const toast = reactive({ visible: false, message: '', type: 'success' })
const lastIds = reactive({ user_id: null, organization_id: null, department_id: null, document_id: null })

const registerForm  = reactive({ full_name: '', email: '', phone: '', password: '', role: 'employee' })
const loginForm     = reactive({ email: '', password: '' })
const organizationForm = reactive({ name: '' })
const departmentForm   = reactive({ organization_id: null, name: '' })
const inviteForm       = reactive({ user_id: null, organization_id: null })
const roleForm = reactive({
  user_id: null, organization_id: null, department_id: null,
  role_name: '', can_send_document: false, can_sign_document: false, can_manage_department: false
})
const documentForm = reactive({ title: '', content: '', link: '', organization_id: null, department_id: null })
const sendForm     = reactive({ document_id: null, organization_id: null, department_id: null, recipient_user_id: null })
const signForm     = reactive({ document_id: null })
const statusForm   = reactive({ document_id: null, recipient_user_id: null })

// ---- COMPUTED ----
const isAdmin    = computed(() => userRole.value === 'admin')
const isBoss     = computed(() => userRole.value === 'boss')
const isEmployee = computed(() => userRole.value === 'employee')

const roleIcon  = computed(() => ({ admin: '🛡️', boss: '👔', employee: '👤' }[userRole.value] || '👤'))
const roleLabel = computed(() => ({ admin: 'Администратор', boss: 'Начальник', employee: 'Сотрудник' }[userRole.value] || userRole.value))
const firstName = computed(() => (currentUser.value?.full_name ?? '').split(' ')[0])
const roleDescription = computed(() => ({
  admin: 'Администратор — полный контроль системы',
  boss: 'Начальник — создание и отправка документов',
  employee: 'Сотрудник — подписание документов'
})[userRole.value] || '')

const newCount = computed(() => inboxList.value.filter(d => !d.status || d.status === 'new').length)

const visibleTabs = computed(() => {
  const common = [
    { key: 'home',          label: 'Главная' },
    { key: 'inbox',         label: 'Полученные письма', badge: true },
    { key: 'read_unsigned', label: 'Не подписанные' },
    { key: 'signed',        label: 'Подписанные' },
  ]
  // Босс не получает отдельную вкладку — форма уже на главной
  if (isEmployee.value) return [...common, { key: 'sign',       label: 'Подписать' }]
  if (isAdmin.value)    return [...common, { key: 'admin_info', label: 'Мониторинг' }]
  return common
})

const shortOutput = computed(() => {
  if (!output.value) return '—'
  const s = JSON.stringify(output.value)
  return s.length > 140 ? s.slice(0, 140) + '…' : s
})

// ---- HELPERS ----
function docStatusLabel(s) {
  return { new: 'Новое', pending: 'На подписи', signed: 'Подписан', read: 'Прочитано' }[s] || 'Новое'
}
function statusClass(s) {
  return { new: 'doc-status--new', pending: 'doc-status--pending', signed: 'doc-status--signed', read: 'doc-status--read' }[s] || 'doc-status--new'
}
function toggleTheme() { theme.value = theme.value === 'light' ? 'dark' : 'light' }
function pretty(v) { return v == null ? 'Нет данных' : JSON.stringify(v, null, 2) }
function clearOutput() { output.value = null }
function logout() { token.value = null; currentUser.value = null; userRole.value = ''; authMode.value = 'login'; authError.value = '' }

function showToast(message, type = 'success') {
  toast.message = message; toast.type = type; toast.visible = true
  setTimeout(() => { toast.visible = false }, 3500)
}

function switchTab(key) {
  activeTab.value = key
  if (key === 'inbox')         loadInbox()
  if (key === 'read_unsigned') loadPending()
  if (key === 'signed')        loadSigned()
  if (key === 'admin_info')    loadAllUsers()
}

function normalizeError(data) {
  if (!data) return 'Неизвестная ошибка'
  if (typeof data === 'string') return data
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) return data.detail.map(i => `${(i.loc||[]).join(' → ')}: ${i.msg}`).join('\n')
  return JSON.stringify(data, null, 2)
}

function setSenderRole() { roleForm.role_name = 'sender'; roleForm.can_send_document = true;  roleForm.can_sign_document = false; roleForm.can_manage_department = false }
function setSignerRole()  { roleForm.role_name = 'signer'; roleForm.can_send_document = false; roleForm.can_sign_document = true;  roleForm.can_manage_department = false }

async function onDocOrgChange() {
  const orgId = documentForm.organization_id
  sendForm.organization_id = orgId
  lastIds.organization_id = orgId
  loadDepartmentsByOrg(orgId)
  await loadUsersByOrg(orgId)
}

// ---- API ----
async function apiRequest(path, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' }
  if (token.value) headers['Authorization'] = `Bearer ${token.value}`
  const options = { method, headers }
  if (body !== null) options.body = JSON.stringify(body)
  const response = await fetch(`${baseUrl.value}${path}`, options)
  let data
  try { data = await response.json() } catch { data = { detail: 'Сервер вернул не JSON' } }
  if (!response.ok) {
    const message = normalizeError(data)
    output.value = { status: response.status, error: message, raw: data }
    throw new Error(message)
  }
  output.value = data
  return data
}

// ---- AUTH ----
async function registerUser() {
  authLoading.value = true; authError.value = ''
  try {
    await apiRequest('/auth/register', 'POST', registerForm)
    loginForm.email = registerForm.email
    loginForm.password = registerForm.password
    authMode.value = 'login'
    showToast('Регистрация успешна!')
  } catch(e) { authError.value = e.message } finally { authLoading.value = false }
}

async function login() {
  authLoading.value = true; authError.value = ''
  try {
    const data = await apiRequest('/auth/login', 'POST', loginForm)
    if (!data?.access_token) throw new Error('Нет токена в ответе')
    token.value    = data.access_token
    userRole.value = data.role ?? 'employee'
    currentUser.value = { id: data.user_id, full_name: data.full_name, email: data.email, role: data.role }
    lastIds.user_id   = data.user_id
    activeTab.value   = 'home'
    loadInbox(); loadPending(); loadSigned(); loadOutbox()
    loadOrganizations()
    if (userRole.value === 'admin') { loadAllUsers() }
  } catch(e) { authError.value = e.message } finally { authLoading.value = false }
}

// ---- ORGANIZATIONS ----
async function loadOrganizations() {
  try {
    const d = await apiRequest('/organizations/')
    organizations.value = Array.isArray(d) ? d : []
    if (organizations.value.length === 1) {
      const orgId = organizations.value[0].id
      documentForm.organization_id = orgId
      sendForm.organization_id = orgId
      lastIds.organization_id = orgId
      loadDepartmentsByOrg(orgId)
      loadUsersByOrg(orgId)
    }
  } catch(e) { showToast(e.message, 'error') }
}

async function createOrganization() {
  if (!organizationForm.name.trim()) return showToast('Укажите название', 'error')
  try {
    const data = await apiRequest('/organizations/', 'POST', { name: organizationForm.name })
    if (data?.id) {
      lastIds.organization_id = data.id
      departmentForm.organization_id = data.id
      inviteForm.organization_id = data.id
      roleForm.organization_id = data.id
      documentForm.organization_id = data.id
      sendForm.organization_id = data.id
    }
    showToast('Организация создана!')
    loadOrganizations()
  } catch(e) { showToast(e.message, 'error') }
}

async function deleteOrganization(id) {
  try {
    await apiRequest(`/organizations/${id}`, 'DELETE')
    showToast('Организация удалена')
    loadOrganizations()
  } catch(e) { showToast(e.message, 'error') }
}

// ---- DEPARTMENTS ----
async function loadDepartmentsByOrg(orgId) {
  if (!orgId) return
  try {
    const d = await apiRequest(`/departments/by-organization/${orgId}`)
    departments.value = Array.isArray(d) ? d : []
    if (departments.value.length === 1) {
      const deptId = departments.value[0].id
      documentForm.department_id = deptId
      sendForm.department_id = deptId
      lastIds.department_id = deptId
    }
  } catch(e) { departments.value = [] }
}

async function createDepartment() {
  if (!departmentForm.organization_id || !departmentForm.name.trim()) return showToast('Заполните организацию и название', 'error')
  try {
    const data = await apiRequest('/departments/', 'POST', {
      organization_id: departmentForm.organization_id,
      name: departmentForm.name
    })
    if (data?.id) {
      lastIds.department_id = data.id
      roleForm.department_id = data.id
      documentForm.department_id = data.id
      sendForm.department_id = data.id
    }
    showToast('Отдел создан!')
    loadDepartmentsByOrg(departmentForm.organization_id)
  } catch(e) { showToast(e.message, 'error') }
}

// ---- USERS BY ORG ----
async function loadUsersByOrg(orgId) {
  if (!orgId) return
  orgUsers.value = []
  usersLoading.value = true
  try {
    let users = []
    try {
      const d = await apiRequest(`/employees/by-organization/${orgId}`)
      users = Array.isArray(d) ? d : []
    } catch {
      try {
        const d = await apiRequest('/auth/users')
        users = Array.isArray(d) ? d : []
        if (isAdmin.value) allUsers.value = users
      } catch {
        users = []
      }
    }
    orgUsers.value = users
  } finally {
    usersLoading.value = false
  }
}

// ---- EMPLOYEES ----
async function inviteEmployee() {
  if (!inviteForm.user_id || !inviteForm.organization_id) return showToast('Выберите пользователя и организацию', 'error')
  try {
    await apiRequest('/employees/invite', 'POST', inviteForm)
    showToast('Сотрудник приглашён!')
  } catch(e) { showToast(e.message, 'error') }
}

// ---- ACCESS/ROLES ----
async function assignRole() {
  if (!roleForm.user_id) return showToast('Выберите пользователя', 'error')
  if (!roleForm.organization_id) return showToast('Выберите организацию', 'error')
  if (!roleForm.department_id) return showToast('Выберите отдел', 'error')
  if (!roleForm.role_name.trim()) return showToast('Укажите название роли', 'error')
  try {
    await apiRequest('/access/assign-role', 'POST', roleForm)
    showToast('Роль выдана!')
  } catch(e) { showToast(e.message, 'error') }
}

// ---- DOCUMENTS ----

async function createAndSend() {
  if (!documentForm.title.trim()) return showToast('Укажите заголовок', 'error')
  if (!documentForm.content?.trim() && !documentForm.link?.trim()) return showToast('Укажите текст или ссылку', 'error')
  const orgId  = parseInt(documentForm.organization_id, 10)
  const deptId = parseInt(documentForm.department_id, 10)
  if (!orgId  || orgId  <= 0) return showToast('Выберите организацию', 'error')
  if (!deptId || deptId <= 0) return showToast('Выберите отдел', 'error')
  if (!sendForm.recipient_user_id)  return showToast('Выберите получателя', 'error')

  sendLoading.value = true
  try {
    const doc = await apiRequest('/documents/create', 'POST', {
      title: documentForm.title,
      content: documentForm.content || '',
      link: documentForm.link || null,
      organization_id: orgId,
      department_id: deptId,
    })
    const docId = doc.id
    lastIds.document_id = docId
    sentDocuments.value.push({ id: docId, title: documentForm.title })

    await apiRequest('/documents/send', 'POST', {
      document_id: docId,
      organization_id: orgId,
      department_id: deptId,
      recipient_user_id: parseInt(sendForm.recipient_user_id, 10),
    })

    showToast('Документ создан и отправлен!')
    documentForm.title = ''
    documentForm.content = ''
    documentForm.link = ''
    sendForm.recipient_user_id = null
  } catch(e) {
    showToast(e.message, 'error')
  } finally {
    sendLoading.value = false
  }
}

async function signDocument() {
  if (!signForm.document_id) return showToast('Укажите ID документа', 'error')
  try {
    await apiRequest('/signatures/sign', 'POST', { document_id: signForm.document_id })
    loadPending(); loadInbox(); loadSigned()
    showToast('Документ подписан!')
  } catch(e) { showToast(e.message, 'error') }
}

async function quickSign(docId) {
  signForm.document_id = docId
  await signDocument()
}

async function loadInbox() {
  if (!lastIds.user_id) return
  try {
    const d = await apiRequest('/documents/inbox', 'POST', { user_id: lastIds.user_id })
    inboxList.value = Array.isArray(d) ? d : []
  } catch { inboxList.value = [] }
}

async function loadOutbox() {
  if (!lastIds.user_id) return
  try {
    const d = await apiRequest('/documents/outbox', 'POST', { user_id: lastIds.user_id })
    outboxList.value = Array.isArray(d) ? d : []
  } catch { outboxList.value = [] }
}

async function loadSigned() {
  if (!lastIds.user_id) return
  try {
    const d = await apiRequest('/documents/inbox', 'POST', { user_id: lastIds.user_id })
    const all = Array.isArray(d) ? d : []
    signedList.value = all.filter(doc => doc.status === 'signed')
  } catch { signedList.value = [] }
}

async function loadPending() {
  if (!lastIds.user_id) return
  try {
    const d = await apiRequest('/documents/pending', 'POST', { user_id: lastIds.user_id })
    pendingList.value = Array.isArray(d) ? d : []
  } catch { pendingList.value = [] }
}

async function loadStatus() {
  if (!statusForm.document_id || !statusForm.recipient_user_id) return showToast('Укажите ID документа и получателя', 'error')
  try {
    statusResult.value = await apiRequest(`/documents/status/${statusForm.document_id}/${statusForm.recipient_user_id}`)
  } catch(e) { showToast(e.message, 'error') }
}

async function loadAllUsers() {
  if (!isAdmin.value) return
  try {
    const d = await apiRequest('/auth/users')
    allUsers.value = Array.isArray(d) ? d : []
  } catch(e) { showToast(e.message, 'error') }
}
</script>

<style scoped>
.role-pill {
  display: flex; align-items: center; gap: 5px;
  padding: 4px 10px; border-radius: 99px;
  font-size: 12px; font-weight: 600;
  user-select: none;
}
.role-pill--admin    { background: #fff0f0; color: #c0392b; border: 1px solid rgba(192,57,43,.2); }
.role-pill--boss     { background: #fffbea; color: #b8860b; border: 1px solid rgba(184,134,11,.2); }
.role-pill--employee { background: #e8f4fd; color: #1a7fc4; border: 1px solid rgba(26,127,196,.18); }

.field-label {
  display: flex; flex-direction: column; gap: 5px;
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .06em; color: var(--text-muted);
}
.field-optional { font-weight: 400; text-transform: none; letter-spacing: 0; opacity: .6; }

.form-row {
  display: flex; gap: 12px;
}
.form-row > * { flex: 1; min-width: 0; }

.card--wide { max-width: 640px; }

.hint-warn {
  font-size: 11px; color: #b8860b; font-weight: 500;
  text-transform: none; letter-spacing: 0;
}

.doc-link {
  font-size: 12px; color: var(--primary); text-decoration: none;
  font-weight: 500;
}
.doc-link:hover { text-decoration: underline; }

.mini-list { margin-top: 10px; display: flex; flex-direction: column; gap: 4px; }
.mini-row  { display: flex; align-items: center; gap: 8px; font-size: 13px; padding: 4px 6px; background: var(--bg); border-radius: 6px; }
.mini-name { flex: 1; font-weight: 500; }
.mini-id   { font-size: 11px; color: var(--text-muted); }

.section-title-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.section-title-row .section-title { margin-bottom: 0; }

.kpi-sub { font-size: 11px; color: var(--text-faint); margin-top: 2px; }

.toast {
  position: fixed; top: calc(var(--header-h) + 12px); right: 20px;
  z-index: 300; display: flex; align-items: center; gap: 12px;
  padding: 12px 16px; border-radius: var(--radius-lg);
  font-size: 13px; font-weight: 600; box-shadow: var(--shadow-lg);
  max-width: 380px; border: 1px solid transparent;
}
.toast--success { background: var(--success-tint); color: var(--success); border-color: rgba(30,138,82,.2); }
.toast--error   { background: var(--error-tint);   color: var(--error);   border-color: rgba(181,39,58,.2); }
.toast__close { background: none; border: none; cursor: pointer; font-size: 14px; opacity: .6; color: inherit; margin-left: auto; }
.toast__close:hover { opacity: 1; }

.spinner { animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.fade-enter-active, .fade-leave-active { transition: opacity .25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.tab-fade-enter-active, .tab-fade-leave-active { transition: opacity .18s ease, transform .18s ease; }
.tab-fade-enter-from { opacity: 0; transform: translateY(6px); }
.tab-fade-leave-to   { opacity: 0; transform: translateY(-4px); }

.slide-down-enter-active, .slide-down-leave-active { transition: all .22s ease; }
.slide-down-enter-from { opacity: 0; transform: translateY(-12px); }
.slide-down-leave-to   { opacity: 0; transform: translateY(-12px); }

.slide-up-enter-active, .slide-up-leave-active { transition: all .22s ease; }
.slide-up-enter-from { opacity: 0; transform: translateY(8px); }
.slide-up-leave-to   { opacity: 0; transform: translateY(8px); }
</style>
