<template>
  <div id="app" :data-theme="theme">

    <!-- ===== LOGIN SCREEN ===== -->
    <div v-if="!token" class="auth-screen">
      <div class="auth-card">
        <div class="auth-logo">
          <svg width="44" height="44" viewBox="0 0 44 44" fill="none" aria-label="Флагман">
            <rect width="44" height="44" rx="12" fill="#1a7fc4"/>
            <path d="M10 34V10h18l-6 8h-6v16H10z" fill="white"/>
            <path d="M22 10h12l-6 8H22l6-8z" fill="white" opacity="0.65"/>
          </svg>
          <span class="auth-logo__text">Флагман</span>
        </div>
        <p class="auth-subtitle">Сервис рассылки и подписания документов</p>

        <div v-if="authMode === 'login'" class="auth-form">
          <h2>Войти в аккаунт</h2>
          <label>Email
            <input v-model="loginForm.email" class="input" type="email" placeholder="you@company.ru" />
          </label>
          <label>Пароль
            <input v-model="loginForm.password" class="input" type="password" placeholder="••••••••" />
          </label>
          <div class="auth-backend">
            <label>Backend URL
              <input v-model="baseUrl" class="input input--sm" placeholder="http://127.0.0.1:8000" />
            </label>
          </div>
          <button class="btn btn--primary btn--full" @click="login" :disabled="authLoading">
            {{ authLoading ? 'Входим...' : 'Войти' }}
          </button>
          <p class="auth-switch">Нет аккаунта? <button class="link-btn" @click="authMode = 'register'">Зарегистрироваться</button></p>
          <p v-if="authError" class="error-msg">{{ authError }}</p>
        </div>

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
          <div class="auth-backend">
            <label>Backend URL
              <input v-model="baseUrl" class="input input--sm" placeholder="http://127.0.0.1:8000" />
            </label>
          </div>
          <button class="btn btn--primary btn--full" @click="registerUser" :disabled="authLoading">
            {{ authLoading ? 'Регистрируемся...' : 'Зарегистрироваться' }}
          </button>
          <p class="auth-switch">Уже есть аккаунт? <button class="link-btn" @click="authMode = 'login'">Войти</button></p>
          <p v-if="authError" class="error-msg">{{ authError }}</p>
        </div>
      </div>
    </div>

    <!-- ===== MAIN APP ===== -->
    <div v-else class="app-layout">

      <!-- TOP HEADER -->
      <header class="header">
        <div class="header__left">
          <svg width="32" height="32" viewBox="0 0 44 44" fill="none">
            <rect width="44" height="44" rx="10" fill="#1a7fc4"/>
            <path d="M10 34V10h18l-6 8h-6v16H10z" fill="white"/>
            <path d="M22 10h12l-6 8H22l6-8z" fill="white" opacity="0.65"/>
          </svg>
          <span class="header__brand">Флагман</span>
        </div>

        <!-- ROLE TABS (top nav) -->
        <nav class="header__tabs" v-if="userRole">
          <button
            v-for="tab in visibleTabs"
            :key="tab.key"
            class="header__tab"
            :class="{ active: activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
            <span v-if="tab.badge && inboxList.length" class="badge">{{ inboxList.filter(d => d.status === 'pending').length || '' }}</span>
          </button>
        </nav>

        <div class="header__right">
          <div class="role-pill">
            <span class="role-icon">{{ roleIcon }}</span>
            <select v-model="userRole" class="role-select">
              <option value="admin">Администратор</option>
              <option value="manager">Начальник</option>
              <option value="employee">Сотрудник</option>
            </select>
          </div>
          <div class="user-info">
            <span class="user-name">{{ currentUser?.full_name ?? currentUser?.email ?? 'Пользователь' }}</span>
          </div>
          <button class="btn btn--ghost btn--sm" @click="logout">Выйти</button>
          <button class="icon-btn" @click="toggleTheme" :title="theme === 'light' ? 'Тёмная тема' : 'Светлая тема'">
            <svg v-if="theme === 'light'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          </button>
        </div>
      </header>

      <!-- PAGE CONTENT -->
      <main class="page">

        <!-- ============ HOME ============ -->
        <section v-if="activeTab === 'home'">
          <div class="page-header">
            <h1>Главная</h1>
            <p class="page-sub">Обзор системы и быстрые действия</p>
          </div>

          <div class="kpi-row">
            <div class="kpi-card">
              <span class="kpi-label">Входящих</span>
              <span class="kpi-value">{{ inboxList.length }}</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Ожидают подписи</span>
              <span class="kpi-value kpi-value--warn">{{ pendingList.length }}</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Исходящих</span>
              <span class="kpi-value">{{ outboxList.length }}</span>
            </div>
            <div class="kpi-card" v-if="userRole === 'admin'">
              <span class="kpi-label">Backend</span>
              <span class="kpi-value kpi-value--ok">● Online</span>
            </div>
          </div>

          <!-- Admin: quick structure management -->
          <div v-if="userRole === 'admin'" class="section-block">
            <h2 class="section-title">Управление структурой</h2>
            <div class="cards-grid">
              <div class="card">
                <div class="card__title">Организация</div>
                <div class="form-inline">
                  <input v-model="organizationForm.name" class="input" placeholder="Название организации" />
                  <button class="btn btn--primary" @click="createOrganization">Создать</button>
                </div>
                <p class="hint" v-if="lastIds.organization_id">Текущий org ID: <code>{{ lastIds.organization_id }}</code></p>
              </div>
              <div class="card">
                <div class="card__title">Отдел</div>
                <div class="form-col">
                  <input v-model.number="departmentForm.organization_id" class="input" type="number" placeholder="ID организации" />
                  <input v-model="departmentForm.name" class="input" placeholder="Название отдела" />
                  <button class="btn btn--primary" @click="createDepartment">Создать отдел</button>
                </div>
                <p class="hint" v-if="lastIds.department_id">Текущий dept ID: <code>{{ lastIds.department_id }}</code></p>
              </div>
              <div class="card">
                <div class="card__title">Пригласить сотрудника</div>
                <div class="form-col">
                  <input v-model.number="inviteForm.user_id" class="input" type="number" placeholder="ID пользователя" />
                  <input v-model.number="inviteForm.organization_id" class="input" type="number" placeholder="ID организации" />
                  <button class="btn btn--primary" @click="inviteEmployee">Пригласить</button>
                </div>
              </div>
              <div class="card">
                <div class="card__title">Выдать роль</div>
                <div class="form-col">
                  <input v-model.number="roleForm.user_id" class="input" type="number" placeholder="ID пользователя" />
                  <input v-model.number="roleForm.organization_id" class="input" type="number" placeholder="ID организации" />
                  <input v-model.number="roleForm.department_id" class="input" type="number" placeholder="ID отдела" />
                  <input v-model="roleForm.role_name" class="input" placeholder="Название роли" />
                  <div class="checks-row">
                    <label class="check-label"><input type="checkbox" v-model="roleForm.can_send_document" /><span>Отправка</span></label>
                    <label class="check-label"><input type="checkbox" v-model="roleForm.can_sign_document" /><span>Подпись</span></label>
                    <label class="check-label"><input type="checkbox" v-model="roleForm.can_manage_department" /><span>Управление</span></label>
                  </div>
                  <div class="btn-row">
                    <button class="btn btn--ghost btn--sm" @click="setSenderRole">Роль: Начальник</button>
                    <button class="btn btn--ghost btn--sm" @click="setSignerRole">Роль: Сотрудник</button>
                  </div>
                  <button class="btn btn--primary" @click="assignRole">Выдать роль</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Admin: backend config -->
          <div v-if="userRole === 'admin'" class="section-block">
            <h2 class="section-title">Настройки Backend</h2>
            <div class="card card--narrow">
              <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">Backend URL
                <input v-model="baseUrl" class="input" placeholder="http://127.0.0.1:8000" />
              </label>
              <div class="ids-list">
                <span>user: <code>{{ lastIds.user_id ?? '—' }}</code></span>
                <span>org: <code>{{ lastIds.organization_id ?? '—' }}</code></span>
                <span>dept: <code>{{ lastIds.department_id ?? '—' }}</code></span>
                <span>doc: <code>{{ lastIds.document_id ?? '—' }}</code></span>
              </div>
            </div>
          </div>

          <!-- Manager: send document -->
          <div v-if="userRole === 'manager'" class="section-block">
            <h2 class="section-title">Создать и отправить документ</h2>
            <div class="cards-grid">
              <div class="card">
                <div class="card__title">Новый документ</div>
                <div class="form-col">
                  <input v-model="documentForm.title" class="input" placeholder="Заголовок документа" />
                  <textarea v-model="documentForm.content" class="input textarea" placeholder="Содержимое документа"></textarea>
                  <input v-model.number="documentForm.organization_id" class="input" type="number" placeholder="ID организации" />
                  <input v-model.number="documentForm.department_id" class="input" type="number" placeholder="ID отдела" />
                  <button class="btn btn--primary" @click="createDocument">Создать документ</button>
                </div>
                <p class="hint" v-if="lastIds.document_id">Создан документ ID: <code>{{ lastIds.document_id }}</code></p>
              </div>
              <div class="card">
                <div class="card__title">Отправить на подпись</div>
                <div class="form-col">
                  <input v-model.number="sendForm.document_id" class="input" type="number" placeholder="ID документа" />
                  <input v-model.number="sendForm.organization_id" class="input" type="number" placeholder="ID организации" />
                  <input v-model.number="sendForm.department_id" class="input" type="number" placeholder="ID отдела" />
                  <input v-model.number="sendForm.recipient_user_id" class="input" type="number" placeholder="ID получателя" />
                  <div class="btn-row">
                    <button class="btn btn--ghost btn--sm" @click="fillSendIds">Подставить последние ID</button>
                  </div>
                  <button class="btn btn--primary" @click="sendDocument">Отправить</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Employee: quick sign -->
          <div v-if="userRole === 'employee'" class="section-block">
            <h2 class="section-title">Требуют подписи</h2>
            <div v-if="pendingList.length" class="doc-list">
              <div v-for="doc in pendingList" :key="doc.document_id" class="doc-row doc-row--pending">
                <div class="doc-row__info">
                  <span class="doc-title">{{ doc.title ?? 'Документ #' + doc.document_id }}</span>
                  <span class="doc-status doc-status--pending">На подписи</span>
                </div>
                <button class="btn btn--primary btn--sm" @click="quickSign(doc.document_id)">Подписать</button>
              </div>
            </div>
            <div v-else class="empty-state">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              <p>Документов, ожидающих вашей подписи, нет</p>
            </div>
          </div>
        </section>

        <!-- ============ ПОЛУЧЕННЫЕ ПИСЬМА ============ -->
        <section v-if="activeTab === 'inbox'">
          <div class="page-header">
            <h1>Полученные письма</h1>
            <p class="page-sub">Входящие документы</p>
            <button class="btn btn--ghost btn--sm" @click="loadInbox">Обновить</button>
          </div>
          <div class="filter-bar">
            <label>ID пользователя
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
              :class="{ 'doc-row--new': doc.status === 'new' || !doc.status }"
            >
              <div class="doc-row__info">
                <span class="doc-title">{{ doc.title ?? 'Документ #' + (doc.document_id ?? doc.id) }}</span>
                <span class="doc-id">ID: {{ doc.document_id ?? doc.id }}</span>
              </div>
              <span
                class="doc-status"
                :class="{
                  'doc-status--new': doc.status === 'new' || !doc.status,
                  'doc-status--pending': doc.status === 'pending',
                  'doc-status--signed': doc.status === 'signed'
                }"
              >{{ docStatusLabel(doc.status) }}</span>
            </div>
          </div>
          <div v-else class="empty-state">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            <p>Нет входящих документов</p>
            <button class="btn btn--ghost btn--sm" @click="loadInbox">Загрузить</button>
          </div>
        </section>

        <!-- ============ ПРОЧИТАННЫЕ, НЕ ПОДПИСАННЫЕ ============ -->
        <section v-if="activeTab === 'read_unsigned'">
          <div class="page-header">
            <h1>Прочитанные, не подписанные</h1>
            <p class="page-sub">Документы, с которыми вы ознакомились, но ещё не подписали</p>
          </div>
          <div class="filter-bar">
            <label>ID пользователя
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
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            <p>Нет документов, ожидающих подписи</p>
          </div>
        </section>

        <!-- ============ ПОДПИСАННЫЕ ============ -->
        <section v-if="activeTab === 'signed'">
          <div class="page-header">
            <h1>Подписанные документы</h1>
            <p class="page-sub">Исходящие документы с завершённым статусом</p>
            <button class="btn btn--ghost btn--sm" @click="loadOutbox">Обновить</button>
          </div>
          <div class="filter-bar">
            <label>ID пользователя
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
              <span class="doc-status doc-status--signed">Подписан ✓</span>
            </div>
          </div>
          <div v-else class="empty-state">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <p>Нет подписанных документов</p>
          </div>
        </section>

        <!-- ============ MANAGER: ОТПРАВИТЬ ДОКУМЕНТ ============ -->
        <section v-if="activeTab === 'send'">
          <div class="page-header">
            <h1>Отправить документ</h1>
            <p class="page-sub">Создайте документ и отправьте сотруднику на подпись</p>
          </div>
          <div class="cards-grid">
            <div class="card">
              <div class="card__title">Шаг 1 — Создать документ</div>
              <div class="form-col">
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">Заголовок
                  <input v-model="documentForm.title" class="input" placeholder="Например: Приказ №12" />
                </label>
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">Содержимое
                  <textarea v-model="documentForm.content" class="input textarea" placeholder="Текст документа..." rows="4"></textarea>
                </label>
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID организации
                  <input v-model.number="documentForm.organization_id" class="input" type="number" placeholder="ID организации" />
                </label>
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID отдела
                  <input v-model.number="documentForm.department_id" class="input" type="number" placeholder="ID отдела" />
                </label>
                <div class="btn-row">
                  <button class="btn btn--ghost btn--sm" @click="fillDocumentTemplate">Шаблон</button>
                  <button class="btn btn--ghost btn--sm" @click="fillDocumentIds">Подставить ID</button>
                </div>
                <button class="btn btn--primary" @click="createDocument">Создать документ</button>
              </div>
              <p class="hint success" v-if="lastIds.document_id">✓ Документ создан, ID: <code>{{ lastIds.document_id }}</code></p>
            </div>
            <div class="card">
              <div class="card__title">Шаг 2 — Отправить получателю</div>
              <div class="form-col">
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID документа
                  <input v-model.number="sendForm.document_id" class="input" type="number" placeholder="ID документа" />
                </label>
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID организации
                  <input v-model.number="sendForm.organization_id" class="input" type="number" placeholder="ID организации" />
                </label>
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID отдела
                  <input v-model.number="sendForm.department_id" class="input" type="number" placeholder="ID отдела" />
                </label>
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID получателя
                  <input v-model.number="sendForm.recipient_user_id" class="input" type="number" placeholder="ID сотрудника" />
                </label>
                <div class="btn-row">
                  <button class="btn btn--ghost btn--sm" @click="fillSendIds">Подставить ID</button>
                </div>
                <button class="btn btn--primary" @click="sendDocument">Отправить на подпись</button>
              </div>
            </div>
          </div>
        </section>

        <!-- ============ EMPLOYEE: ПОДПИСАТЬ ============ -->
        <section v-if="activeTab === 'sign'">
          <div class="page-header">
            <h1>Подписать документ</h1>
            <p class="page-sub">Подписание на основе номера телефона</p>
          </div>
          <div class="card card--narrow">
            <div class="form-col">
              <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID документа
                <input v-model.number="signForm.document_id" class="input" type="number" placeholder="ID документа" />
              </label>
              <div class="btn-row">
                <button class="btn btn--ghost btn--sm" @click="signForm.document_id = lastIds.document_id">Подставить ID</button>
              </div>
              <button class="btn btn--primary" @click="signDocument">Подписать документ</button>
            </div>
          </div>
        </section>

        <!-- ============ ADMIN: ВСЯ ИНФОРМАЦИЯ ============ -->
        <section v-if="activeTab === 'admin_info'">
          <div class="page-header">
            <h1>Информация по системе</h1>
            <p class="page-sub">Полные данные о документах и пользователях</p>
          </div>
          <div class="cards-grid">
            <div class="card">
              <div class="card__title">Статус документа</div>
              <div class="form-col">
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID документа
                  <input v-model.number="statusForm.document_id" class="input" type="number" placeholder="ID документа" />
                </label>
                <label style="display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:500;color:var(--text-muted)">ID получателя
                  <input v-model.number="statusForm.recipient_user_id" class="input" type="number" placeholder="ID получателя" />
                </label>
                <div class="btn-row">
                  <button class="btn btn--ghost btn--sm" @click="fillStatusIds">Подставить ID</button>
                </div>
                <button class="btn btn--primary" @click="loadStatus">Проверить статус</button>
              </div>
              <div v-if="statusResult" class="json-preview">
                <pre>{{ pretty(statusResult) }}</pre>
              </div>
            </div>
            <div class="card">
              <div class="card__title">Ответ сервера</div>
              <div class="json-preview">
                <pre>{{ pretty(output) }}</pre>
              </div>
              <button class="btn btn--ghost btn--sm" style="margin-top:8px" @click="clearOutput">Очистить</button>
            </div>
          </div>
        </section>

      </main>

      <!-- BOTTOM STATUS BAR -->
      <div class="status-bar" v-if="output && userRole === 'admin'">
        <span class="status-bar__label">Последний ответ:</span>
        <code class="status-bar__code">{{ shortOutput }}</code>
        <button class="status-bar__close" @click="clearOutput">✕</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

const baseUrl = ref('http://127.0.0.1:8000')
const activeTab = ref('home')
const token = ref(null)
const currentUser = ref(null)
const authMode = ref('login')
const authLoading = ref(false)
const authError = ref('')
const theme = ref('light')
const userRole = ref('employee')

const output = ref(null)
const inboxList = ref([])
const outboxList = ref([])
const pendingList = ref([])
const statusResult = ref(null)
const inboxUserId = ref(null)
const outboxUserId = ref(null)
const pendingUserId = ref(null)

const lastIds = reactive({
  user_id: null, organization_id: null,
  department_id: null, document_id: null, recipient_user_id: null
})

const registerForm = reactive({ full_name: '', email: '', phone: '', password: '' })
const loginForm = reactive({ email: '', password: '' })
const organizationForm = reactive({ name: '' })
const departmentForm = reactive({ organization_id: null, name: '' })
const inviteForm = reactive({ user_id: null, organization_id: null })
const roleForm = reactive({
  user_id: null, organization_id: null, department_id: null,
  role_name: '', can_send_document: false, can_sign_document: false, can_manage_department: false
})
const documentForm = reactive({ title: '', content: '', organization_id: null, department_id: null })
const sendForm = reactive({ document_id: null, organization_id: null, department_id: null, recipient_user_id: null })
const signForm = reactive({ document_id: null })
const statusForm = reactive({ document_id: null, recipient_user_id: null })

const roleIcon = computed(() => ({ admin: '🛡️', manager: '👔', employee: '👤' }[userRole.value] || '👤'))

const visibleTabs = computed(() => {
  const common = [
    { key: 'home', label: 'Главная' },
    { key: 'inbox', label: 'Полученные письма', badge: true },
    { key: 'read_unsigned', label: 'Прочитанные, не подписанные' },
    { key: 'signed', label: 'Подписанные' },
  ]
  if (userRole.value === 'manager') return [...common, { key: 'send', label: 'Отправить документ' }]
  if (userRole.value === 'employee') return [...common, { key: 'sign', label: 'Подписать' }]
  if (userRole.value === 'admin') return [...common, { key: 'admin_info', label: 'Вся информация' }]
  return common
})

const shortOutput = computed(() => {
  if (!output.value) return '—'
  const s = JSON.stringify(output.value)
  return s.length > 120 ? s.slice(0, 120) + '…' : s
})

function docStatusLabel(status) {
  const map = { new: 'Новое', pending: 'На подписи', signed: 'Подписан', read: 'Прочитано' }
  return map[status] || (status ? status : 'Новое')
}

function toggleTheme() { theme.value = theme.value === 'light' ? 'dark' : 'light' }
function pretty(v) { return (v === null || v === undefined) ? 'Нет данных' : JSON.stringify(v, null, 2) }
function clearOutput() { output.value = null }
function logout() { token.value = null; currentUser.value = null; authMode.value = 'login'; authError.value = '' }

function normalizeError(data) {
  if (!data) return 'Неизвестная ошибка'
  if (typeof data === 'string') return data
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) return data.detail.map(i => `${(i.loc||[]).join(' -> ')}: ${i.msg}`).join('\n')
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

function fillDocumentTemplate() { documentForm.title = 'Приказ о внутреннем ознакомлении'; documentForm.content = 'Сотруднику необходимо ознакомиться с документом и подписать его.' }
function fillDocumentIds() { documentForm.organization_id = lastIds.organization_id; documentForm.department_id = lastIds.department_id }
function fillSendIds() { sendForm.document_id = lastIds.document_id; sendForm.organization_id = lastIds.organization_id; sendForm.department_id = lastIds.department_id; sendForm.recipient_user_id = lastIds.recipient_user_id ?? lastIds.user_id }
function fillStatusIds() { statusForm.document_id = lastIds.document_id; statusForm.recipient_user_id = lastIds.recipient_user_id ?? lastIds.user_id }
function setSenderRole() { roleForm.role_name = 'sender'; roleForm.can_send_document = true; roleForm.can_sign_document = false; roleForm.can_manage_department = false }
function setSignerRole() { roleForm.role_name = 'signer'; roleForm.can_send_document = false; roleForm.can_sign_document = true; roleForm.can_manage_department = false }

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
  } catch(e) { authError.value = e.message } finally { authLoading.value = false }
}

async function login() {
  authLoading.value = true; authError.value = ''
  try {
    const data = await apiRequest('/auth/login', 'POST', loginForm)
    if (data?.access_token) {
      token.value = data.access_token
      const me = await apiRequest('/auth/me', 'GET')
      currentUser.value = me; lastIds.user_id = me.id
      inboxUserId.value = me.id; outboxUserId.value = me.id; pendingUserId.value = me.id
      activeTab.value = 'home'
      loadInbox(); loadPending(); loadOutbox()
    }
  } catch(e) { authError.value = e.message } finally { authLoading.value = false }
}

async function createOrganization() {
  try {
    const data = await apiRequest('/organizations/create', 'POST', organizationForm)
    if (data?.id) { lastIds.organization_id = data.id; departmentForm.organization_id = data.id; inviteForm.organization_id = data.id; roleForm.organization_id = data.id; documentForm.organization_id = data.id; sendForm.organization_id = data.id }
  } catch {}
}

async function createDepartment() {
  try {
    const data = await apiRequest('/departments/create', 'POST', departmentForm)
    if (data?.id) { lastIds.department_id = data.id; roleForm.department_id = data.id; documentForm.department_id = data.id; sendForm.department_id = data.id }
  } catch {}
}

async function inviteEmployee() { try { await apiRequest('/employees/invite', 'POST', inviteForm) } catch {} }
async function assignRole() { try { await apiRequest('/access/assign-role', 'POST', roleForm) } catch {} }

async function createDocument() {
  try {
    const data = await apiRequest('/documents/create', 'POST', documentForm)
    if (data?.id) { lastIds.document_id = data.id; sendForm.document_id = data.id }
  } catch {}
}

async function sendDocument() { try { await apiRequest('/documents/send', 'POST', sendForm) } catch {} }
async function signDocument() { try { await apiRequest('/signatures/sign', 'POST', signForm); loadPending() } catch {} }
async function quickSign(docId) { signForm.document_id = docId; await signDocument() }

async function loadInbox() {
  const uid = inboxUserId.value ?? lastIds.user_id
  if (!uid) return
  try { const d = await apiRequest(`/documents/inbox/${uid}`); inboxList.value = Array.isArray(d) ? d : [] } catch { inboxList.value = [] }
}

async function loadOutbox() {
  const uid = outboxUserId.value ?? lastIds.user_id
  if (!uid) return
  try { const d = await apiRequest(`/documents/outbox/${uid}`); outboxList.value = Array.isArray(d) ? d : [] } catch { outboxList.value = [] }
}

async function loadPending() {
  const uid = pendingUserId.value ?? lastIds.user_id
  if (!uid) return
  try { const d = await apiRequest(`/documents/pending/${uid}`); pendingList.value = Array.isArray(d) ? d : [] } catch { pendingList.value = [] }
}

async function loadStatus() {
  try { statusResult.value = await apiRequest(`/documents/status/${statusForm.document_id}/${statusForm.recipient_user_id}`) } catch {}
}
</script>