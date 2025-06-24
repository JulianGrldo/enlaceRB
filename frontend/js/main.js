// App initialization
// --- STATE & CONFIG ---
const state = {
    currentUser: {
        name: 'Usuario de Prueba',
        role: 'Auxiliar' // Default role
    },
    permissions: {
        'Auxiliar': {
            views: ['dashboard', 'hr', 'docs', 'indicators'],
            canRequestVacancy: false, canEvaluateTeam: false, canManageEmployees: false, canAccessPayroll: false, canAccessHrAnalytics: false, canTerminate: false,
        },
        'Analista': {
            views: ['dashboard', 'hr', 'docs', 'indicators'],
            canRequestVacancy: false, canEvaluateTeam: false, canManageEmployees: false, canAccessPayroll: false, canAccessHrAnalytics: false, canTerminate: false,
        },
        'Senior': {
            views: ['dashboard', 'hr', 'docs', 'indicators'],
            canRequestVacancy: false, canEvaluateTeam: false, canManageEmployees: false, canAccessPayroll: false, canAccessHrAnalytics: false, canTerminate: false,
        },
        'Coordinador': {
            views: ['dashboard', 'hr', 'docs', 'indicators'],
            canRequestVacancy: true, canEvaluateTeam: true, canManageEmployees: true, canAccessPayroll: false, canAccessHrAnalytics: false, canTerminate: true,
        },
        'Gerente': {
            views: ['dashboard', 'hr', 'docs', 'indicators', 'admin'],
            canRequestVacancy: true, canEvaluateTeam: true, canManageEmployees: true, canAccessPayroll: true, canAccessHrAnalytics: true, canTerminate: true,
        },
        'Socio': {
            views: ['dashboard', 'hr', 'docs', 'indicators', 'admin'],
            canRequestVacancy: true, canEvaluateTeam: true, canManageEmployees: true, canAccessPayroll: true, canAccessHrAnalytics: true, canTerminate: true,
        }
    }
};

// --- FUNCTIONS ---

const switchView = (viewId) => {
    const views = document.querySelectorAll('.app-view');
    views.forEach(view => view.classList.add('hidden'));
    const targetView = document.getElementById(viewId);
    if (targetView) targetView.classList.remove('hidden');

    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        link.classList.remove('active');
        if (link.dataset.view === viewId) link.classList.add('active');
    });

    if (viewId === 'hr-view') switchHrSubView('hr-update-data-view');
};

const switchHrSubView = (subViewId) => {
    const hrSubViews = document.querySelectorAll('.hr-sub-view');
    hrSubViews.forEach(view => view.classList.add('hidden'));
    const targetSubView = document.getElementById(subViewId);
    if(targetSubView) targetSubView.classList.remove('hidden');

    const hrSubLinks = document.querySelectorAll('.hr-sub-link');
    hrSubLinks.forEach(link => {
        link.classList.toggle('font-bold', link.dataset.subview === subViewId);
        link.classList.toggle('text-rb-blue-main', link.dataset.subview === subViewId);
    });
};

const applyPermissions = () => {
    const role = state.currentUser.role;
    const name = state.currentUser.name;
    const userPermissions = state.permissions[role];

    // Update user display in sidebar and header
    const userNameSidebar = document.getElementById('user-name-sidebar');
    const userRoleSidebar = document.getElementById('user-role-sidebar');
    const welcomeMessage = document.getElementById('welcome-message');
    const userPhotoSidebar = document.getElementById('user-photo-sidebar');
    
    if(userNameSidebar) userNameSidebar.textContent = name;
    if(userRoleSidebar) userRoleSidebar.textContent = role;
    if(welcomeMessage) welcomeMessage.textContent = `Bienvenido, ${name}`;
    if(userPhotoSidebar) userPhotoSidebar.src = `https://placehold.co/80x80/00a9ce/ffffff?text=${name.charAt(0)}`;

    // Show/hide admin menu
    const adminMenu = document.getElementById('admin-menu');
    if(adminMenu) adminMenu.classList.toggle('hidden', !userPermissions.views.includes('admin'));
    
    // --- HR Permissions ---
    const vacancyRequestSubLink = document.querySelector('[data-subview="hr-recruitment-view"]');
    if(vacancyRequestSubLink?.parentElement) vacancyRequestSubLink.parentElement.style.display = userPermissions.canRequestVacancy ? 'block' : 'none';

    const teamEvaluationBtn = document.querySelector('.team-evaluation-btn');
    if (teamEvaluationBtn) teamEvaluationBtn.style.display = userPermissions.canEvaluateTeam ? 'inline-flex' : 'none';

    const hrManagementSection = document.querySelector('.hr-management-section');
    if(hrManagementSection) hrManagementSection.style.display = userPermissions.canManageEmployees ? 'block' : 'none';

    const hrPayrollLink = document.querySelector('[data-subview="hr-payroll-view"]');
    if(hrPayrollLink) hrPayrollLink.style.display = userPermissions.canAccessPayroll ? 'block' : 'none';
    
    const hrAdminSection = document.querySelector('.hr-admin-section');
    if(hrAdminSection) hrAdminSection.style.display = userPermissions.canAccessHrAnalytics ? 'block' : 'none';

    const vacancyRequestBtn = document.querySelector('[data-view-target="hr-vacancy-request-view"]');
    if (vacancyRequestBtn) {
        vacancyRequestBtn.disabled = !userPermissions.canRequestVacancy;
        vacancyRequestBtn.classList.toggle('opacity-50', !userPermissions.canRequestVacancy);
        vacancyRequestBtn.title = !userPermissions.canRequestVacancy ? 'No tiene permiso para esta acción' : '';
    }
};

const handleRoleChange = (event) => {
    state.currentUser.role = event.target.value;
    applyPermissions();

    const currentView = document.querySelector('.app-view:not(.hidden)');
    if (currentView) {
        const currentViewId = currentView.id.replace('-view', '');
         if (!state.permissions[state.currentUser.role].views.includes(currentViewId)) {
            switchView('dashboard-view');
        }
    }
};

const initCalendar = () => {
    const calendarContainer = document.getElementById('calendar-container');
    if(!calendarContainer) return;
    const now = new Date();
    let month = now.getMonth();
    let year = now.getFullYear();
    const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

    const renderCalendar = () => {
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        let calendarHTML = `<div class="flex justify-between items-center mb-4"><button id="prev-month" class="p-1 rounded-full hover:bg-gray-200"><span class="material-symbols-outlined">chevron_left</span></button><h4 class="font-semibold">${monthNames[month]} ${year}</h4><button id="next-month" class="p-1 rounded-full hover:bg-gray-200"><span class="material-symbols-outlined">chevron_right</span></button></div><div class="grid grid-cols-7 text-center text-sm text-gray-500"><div>Do</div><div>Lu</div><div>Ma</div><div>Mi</div><div>Ju</div><div>Vi</div><div>Sá</div></div><div class="grid grid-cols-7 text-center mt-2">`;
        for (let i = 0; i < (firstDay === 0 ? 6 : firstDay - 1); i++) calendarHTML += '<div></div>';
        for (let day = 1; day <= daysInMonth; day++) {
            const isToday = day === now.getDate() && month === now.getMonth() && year === now.getFullYear();
            calendarHTML += `<div class="p-1 ${isToday ? 'bg-rb-cyan text-white rounded-full' : ''}">${day}</div>`;
        }
        calendarHTML += `</div>`;
        calendarContainer.innerHTML = calendarHTML;
        document.getElementById('prev-month').addEventListener('click', () => { month--; if (month < 0) { month = 11; year--; } renderCalendar(); });
        document.getElementById('next-month').addEventListener('click', () => { month++; if (month > 11) { month = 0; year++; } renderCalendar(); });
    };
    renderCalendar();
};

const initInteractiveCarousel = () => {
    const carousel = document.getElementById('announcements-carousel');
    if (!carousel) return;

    const slides = carousel.querySelectorAll('.carousel-slide');
    const prevBtn = document.getElementById('carousel-prev');
    const nextBtn = document.getElementById('carousel-next');
    const dotsContainer = document.getElementById('carousel-dots');
    let currentSlide = 0;
    let slideInterval;

    if (slides.length === 0) return;

    // Create dots
    slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.classList.add('w-3', 'h-3', 'rounded-full', 'bg-gray-300', 'hover:bg-gray-500');
        dot.addEventListener('click', () => {
            goToSlide(i);
        });
        dotsContainer.appendChild(dot);
    });
    const dots = dotsContainer.querySelectorAll('button');

    const goToSlide = (n) => {
        slides[currentSlide].classList.remove('active');
        dots[currentSlide].classList.remove('bg-rb-blue-main');
        dots[currentSlide].classList.add('bg-gray-300');
        
        currentSlide = (n + slides.length) % slides.length;

        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('bg-rb-blue-main');
        dots[currentSlide].classList.remove('bg-gray-300');
        resetInterval();
    };

    const resetInterval = () => {
        clearInterval(slideInterval);
        slideInterval = setInterval(() => goToSlide(currentSlide + 1), 5000);
    };

    prevBtn.addEventListener('click', () => goToSlide(currentSlide - 1));
    nextBtn.addEventListener('click', () => goToSlide(currentSlide + 1));

    goToSlide(0); // Initialize first slide
};

const showModal = (title, content) => {
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    
    if (modalTitle) modalTitle.textContent = title;
    if (modalBody) modalBody.innerHTML = content;
    if (modal) modal.classList.add('flex');
    if (modal) modal.classList.remove('hidden');
};

const hideModal = () => {
    const modal = document.getElementById('modal');
    if (modal) modal.classList.add('hidden');
    if (modal) modal.classList.remove('flex');
};

const callGeminiAPI = async (prompt, buttonEl) => {
    const btnText = buttonEl.querySelector('.btn-text');
    const loader = buttonEl.querySelector('.loader');
    if(btnText) btnText.classList.add('hidden');
    if(loader) loader.classList.remove('hidden');
    buttonEl.disabled = true;

    try {
        let chatHistory = [{ role: "user", parts: [{ text: prompt }] }];
        const payload = { contents: chatHistory };
        const apiKey = ""; 
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
        const response = await fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (!response.ok) throw new Error(`API error: ${response.statusText}`);
        const result = await response.json();
        if (result.candidates && result.candidates[0]?.content?.parts[0]) return result.candidates[0].content.parts[0].text;
        else throw new Error("No content received from API.");
    } catch (error) {
        console.error("Gemini API Error:", error);
        showModal("Error de IA", `<p>Hubo un problema al contactar al asistente de IA.</p><p class="mt-2 text-sm text-red-500">${error.message}</p>`);
        return null;
    } finally {
        if(btnText) btnText.classList.remove('hidden');
        if(loader) loader.classList.add('hidden');
        buttonEl.disabled = false;
    }
};

// --- EVENT LISTENERS ---
document.addEventListener('DOMContentLoaded', () => {
    // Sidebar navigation
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => link.addEventListener('click', (e) => { e.preventDefault(); switchView(link.dataset.view); }));

    // HR sub navigation
    const hrSubLinks = document.querySelectorAll('.hr-sub-link');
    hrSubLinks.forEach(link => link.addEventListener('click', (e) => { e.preventDefault(); switchHrSubView(link.dataset.subview); }));

    // Quick access buttons
    const handleQuickAccess = (e) => {
        e.preventDefault();
        const targetViewId = e.currentTarget.dataset.viewTarget;
        let mainViewId = '';
        if (targetViewId.startsWith('hr-')) mainViewId = 'hr-view';
        else if (targetViewId.startsWith('docs-')) mainViewId = 'docs-view';
        if (mainViewId) { switchView(mainViewId); switchHrSubView(targetViewId); }
    };
    
    const quickAccessBtns = document.querySelectorAll('.quick-access-btn');
    const quickAccessBtnsHr = document.querySelectorAll('.quick-access-btn-hr');
    quickAccessBtns.forEach(btn => btn.addEventListener('click', handleQuickAccess));
    quickAccessBtnsHr.forEach(btn => btn.addEventListener('click', handleQuickAccess));

    // Role selector
    const userRoleSelector = document.getElementById('user-role-selector');
    if(userRoleSelector) userRoleSelector.addEventListener('change', handleRoleChange);

    // AI description generation
    const generateDescBtn = document.getElementById('generate-description-btn');
    if (generateDescBtn) {
        generateDescBtn.addEventListener('click', async () => {
            const vacancyTitle = document.getElementById('vacancy-title').value;
            if (!vacancyTitle) { showModal("Información Requerida", "Por favor, ingrese el 'Nombre del Puesto'."); return; }
            const prompt = `Actúa como un experto en RRHH. Redacta una descripción de puesto profesional y atractiva para el cargo de "${vacancyTitle}". Incluye responsabilidades clave, requisitos y habilidades deseadas.`;
            const description = await callGeminiAPI(prompt, generateDescBtn);
            if (description) document.getElementById('vacancy-description').value = description.replace(/\*/g, '•');
        });
    }
    
    // Paz y salvo generation
    const generatePazYSalvoBtn = document.getElementById('generate-pazysalvo-btn');
    if(generatePazYSalvoBtn) {
        generatePazYSalvoBtn.addEventListener('click', () => {
            const form = document.getElementById('termination-form');
            const employeeName = form.querySelector('input[type="text"]').value || '[Nombre Empleado]';
            const lastDay = form.querySelector('input[type="date"]').value || '[Último Día]';
            const assets = Array.from(document.querySelectorAll('#asset-checklist input[type="checkbox"]')).map(cb => ({ name: cb.dataset.asset, returned: cb.checked }));
            let content = `<h4 class="font-bold text-lg mb-4">PAZ Y SALVO</h4><p class="mb-4">Se certifica que <strong>${employeeName}</strong>, quien laboró hasta el <strong>${lastDay}</strong>, está a paz y salvo con la empresa por:</p><ul class="list-disc list-inside mb-4">`;
            assets.forEach(asset => { content += `<li>${asset.name}: <span class="font-semibold ${asset.returned ? 'text-green-600' : 'text-red-600'}">${asset.returned ? 'Devuelto' : 'Pendiente'}</span></li>`; });
            content += '</ul><p>Se expide a la fecha actual.</p>';
            showModal("Documento de Paz y Salvo", content);
        });
    }
    
    // Notifications dropdown
    const notificationsBtn = document.getElementById('notifications-btn');
    const notificationsDropdown = document.getElementById('notifications-dropdown');
    if (notificationsBtn) {
        notificationsBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationsDropdown.classList.toggle('hidden');
        });
    }
    document.addEventListener('click', () => {
         if (notificationsDropdown && !notificationsDropdown.classList.contains('hidden')) {
            notificationsDropdown.classList.add('hidden');
        }
    });

    // Gallery items
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            if (img) showModal(img.alt, `<img src="${img.src}" alt="${img.alt}" class="w-full h-auto rounded-lg">`);
        });
    });

    // Modal close button
    const modalCloseBtn = document.getElementById('modal-close-btn');
    if(modalCloseBtn) modalCloseBtn.addEventListener('click', hideModal);
    
    const modal = document.getElementById('modal');
    if(modal) modal.addEventListener('click', (e) => { if (e.target === modal) hideModal(); });

    // --- INITIALIZATION ---
    switchView('dashboard-view');
    applyPermissions();
    initCalendar();
    initInteractiveCarousel();
});