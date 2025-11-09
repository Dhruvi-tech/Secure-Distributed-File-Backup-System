// Global Variables
let currentMode = 'simple';
let currentUser = null;
let isLoggedIn = false;

// Store current session data
let sessionData = {
  simple: { files: [], nodes: [] },
  distributed: { files: [], nodes: [] },
  production: { files: [], nodes: [], cluster: {}, logs: [] },
  secure: { files: [], authenticated: false }
};

// Mode Themes
const modeThemes = {
  simple: { gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', accent: '#667eea' },
  distributed: { gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', accent: '#f5576c' },
  production: { gradient: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #ff8a80 100%)', accent: '#fcb69f' },
  secure: { gradient: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #1a1a2e 100%)', accent: '#00ffff' }
};

// API Base URLs for different modes - all using unified server
const apiBases = {
  simple: 'http://localhost:8080/simple', // Simple mode endpoints
  distributed: 'http://localhost:8080/distributed', // Distributed mode endpoints
  production: 'http://localhost:8080/production', // Production mode endpoints
  secure: 'http://localhost:8080/secure' // Secure mode endpoints
};

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
  initializeNavigation();
  initializeUploadZones();
  loadModeData(currentMode);
  createParticles();
});

// Navigation System
function initializeNavigation() {
  const navTabs = document.querySelectorAll('.nav-tab');

  navTabs.forEach(tab => {
    tab.addEventListener('click', function() {
      const newMode = this.dataset.mode;

      if (newMode === currentMode) return;

      // Fade out current content
      const currentContainer = document.getElementById(`${currentMode}-mode`);
      currentContainer.style.opacity = '0';

      setTimeout(() => {
        // Switch mode
        switchMode(newMode);
      }, 300);
    });
  });
}

function switchMode(newMode) {
  // Update current mode
  currentMode = newMode;

  // Update body class for theme
  document.body.className = `mode-${newMode}`;

  // Update navigation
  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.classList.remove('active');
  });
  document.querySelector(`[data-mode="${newMode}"]`).classList.add('active');

  // Show new mode container
  document.querySelectorAll('.mode-container').forEach(container => {
    container.classList.remove('active');
  });

  const newContainer = document.getElementById(`${newMode}-mode`);
  newContainer.classList.add('active');
  newContainer.style.opacity = '1';

  // Load mode-specific data
  loadModeData(newMode);

  // Create success animation
  showNotification(`Switched to ${newMode.charAt(0).toUpperCase() + newMode.slice(1)} Mode`, 'success');
}

// Data Loading Functions
async function loadModeData(mode) {
  try {
    switch (mode) {
      case 'simple':
        await Promise.all([loadFiles('simple'), loadNodes('simple'), updateStats('simple')]);
        break;
      case 'distributed':
        await Promise.all([loadFiles('distributed'), loadNodes('distributed'), updateStats('distributed')]);
        break;
      case 'production':
        await Promise.all([loadProductionStats(), loadClusterNodes(), loadReplicationLogs()]);
        break;
      case 'secure':
        if (isLoggedIn) {
          await loadSecureData();
        }
        break;
    }
  } catch (error) {
    console.error('Error loading mode data:', error);
    // Fallback: show mock data for development
    showMockDataForMode(mode);
  }
}

function showMockDataForMode(mode) {
  console.log(`Loading mock data for ${mode} mode`);

  switch (mode) {
    case 'simple':
      // Mock simple mode data
      updateNodeDisplay('simple', [{
        node_id: 'local',
        status: 'active',
        files_count: 2,
        storage_used: 1024000,
        last_heartbeat: new Date().toISOString()
      }]);
      updateStats('simple');
      break;

    case 'distributed':
      // Mock distributed mode data
      updateNodeDisplay('distributed', [
        {
          node_id: 'node-01',
          status: 'active',
          files_count: 3,
          storage_used: 2048000,
          last_heartbeat: new Date().toISOString()
        },
        {
          node_id: 'node-02',
          status: 'active',
          files_count: 2,
          storage_used: 1536000,
          last_heartbeat: new Date().toISOString()
        }
      ]);
      updateStats('distributed');
      break;

    case 'production':
      loadProductionStats();
      loadClusterNodes();
      loadReplicationLogs();
      break;
  }
}

// File Operations
async function loadFiles(mode) {
  try {
    const response = await fetch(`${apiBases[mode]}/files`);
    const files = await response.json();

    const filesList = document.getElementById(`${mode}-filesList`);
    filesList.innerHTML = files.map(file => `
      <div class="file-item">
        <strong>${file.filename}</strong>
        <div>Size: ${(file.file_size / 1024).toFixed(2)} KB | Node: ${file.node_id}</div>
        <div>Uploaded: ${new Date(file.upload_time).toLocaleString()}</div>
        <button onclick="downloadFile('${file.file_id}', '${file.filename}', '${mode}')"
                class="download-btn">Download</button>
      </div>
    `).join('');

    updateStats(mode);
  } catch (error) {
    document.getElementById(`${mode}-filesList`).innerHTML =
      `<div style="color: #dc3545; padding: 20px;">❌ Error loading files: ${error.message}</div>`;
  }
}

async function loadNodes(mode) {
  try {
    const response = await fetch(`${apiBases[mode]}/nodes`);
    const nodes = await response.json();

    updateNodeDisplay(mode, nodes);
    updateStats(mode);
  } catch (error) {
    console.error('Error loading nodes:', error);
    // Show fallback mock data
    showMockDataForMode(mode);
  }
}

function updateNodeDisplay(mode, nodes) {
  if (!Array.isArray(nodes)) {
    console.error('Nodes data is not an array:', nodes);
    return;
  }

  const nodesList = document.getElementById(`${mode}-nodesList`);
  nodesList.innerHTML = nodes.map(node => `
    <div class="node-item">
      <strong>Node: ${node.node_id}</strong>
      <div class="${node.status === 'active' ? 'status-healthy' : 'status-unhealthy'}">
        Status: ${node.status || 'unknown'}
      </div>
      <div>Files: ${node.files_count || 0}</div>
      <div>Storage: ${((node.storage_used || 0) / 1024 / 1024).toFixed(2)} MB</div>
      <div>Last Heartbeat: ${node.last_heartbeat ? new Date(node.last_heartbeat).toLocaleString() : 'Never'}</div>
    </div>
  `).join('');
}

async function updateStats(mode) {
  try {
    const [filesResponse, nodesResponse] = await Promise.all([
      fetch(`${apiBases[mode]}/files`),
      fetch(`${apiBases[mode]}/nodes`)
    ]);

    const files = await filesResponse.json();
    const nodes = await nodesResponse.json();

    document.getElementById(`${mode}-totalFiles`).textContent = files.length;
    document.getElementById(`${mode}-activeNodes`).textContent = nodes.filter(n => n.status === 'active').length;

    const totalStorage = files.reduce((sum, file) => sum + file.file_size, 0);
    document.getElementById(`${mode}-totalStorage`).textContent = `${(totalStorage / 1024 / 1024).toFixed(2)} MB`;

  } catch (error) {
    console.error('Error updating stats:', error);
  }
}

// Upload Functions
async function uploadFile(mode) {
  const fileInput = document.getElementById(`${mode}-fileInput`);
  const files = fileInput.files;

  if (files.length === 0) {
    showNotification('Please select at least one file', 'error');
    return;
  }

  const progressDiv = document.getElementById(`${mode}-uploadProgress`);
  const progressFill = document.getElementById(`${mode}-progressFill`);
  const progressText = document.getElementById(`${mode}-progressText`);
  const statusDiv = document.getElementById(`${mode}-uploadStatus`);

  progressDiv.style.display = 'block';
  statusDiv.innerHTML = '';

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const formData = new FormData();
    formData.append('file', file);

    try {
      progressText.textContent = `Uploading ${file.name} (${i + 1}/${files.length})...`;
      progressFill.style.width = `${((i + 1) / files.length) * 100}%`;

      const response = await fetch(`${apiBases[mode]}/upload`, {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (response.ok) {
        statusDiv.innerHTML += `<div style="color: #28a745;">✅ ${file.name} uploaded successfully</div>`;
        createUploadParticles();
      } else {
        statusDiv.innerHTML += `<div style="color: #dc3545;">❌ ${file.name}: ${result.error}</div>`;
      }
    } catch (error) {
      statusDiv.innerHTML += `<div style="color: #dc3545;">❌ ${file.name}: ${error.message}</div>`;
    }
  }

  progressDiv.style.display = 'none';
  loadModeData(mode);
  fileInput.value = '';
}

// Production Mode Functions
async function loadProductionStats() {
  try {
    const [filesResponse, nodesResponse] = await Promise.all([
      fetch(`${apiBases.production}/files`),
      fetch(`${apiBases.production}/nodes`)
    ]);

    const files = await filesResponse.json();
    const nodes = await nodesResponse.json();

    const masterNodes = nodes.filter(n => n.node_id === 'master');
    const slaveNodes = nodes.filter(n => n.node_id !== 'master');

    document.getElementById('production-masterNode').textContent = masterNodes.length;
    document.getElementById('production-slaveNodes').textContent = slaveNodes.length;
    document.getElementById('production-replicationStatus').textContent = 'Healthy';
  } catch (error) {
    console.error('Error loading production stats:', error);
  }
}

async function loadClusterNodes() {
  try {
    const response = await fetch(`${apiBases.production}/cluster`);
    const clusterData = await response.json();

    const clusterGrid = document.getElementById('production-clusterGrid');

    // Master node
    const masterNode = `
      <div class="cluster-node master">
        <div class="node-title">Master Node ${clusterData.master.node_id}</div>
        <div class="node-stats">
          <div>Files: ${clusterData.master.files}</div>
          <div>Chunks: ${clusterData.master.chunks}</div>
          <div>Status: ${clusterData.master.status}</div>
          <div>Last Sync: ${new Date(clusterData.master.last_sync).toLocaleTimeString()}</div>
        </div>
        <div class="status-indicator healthy"></div>
      </div>
    `;

    // Slave nodes
    const slaveNodes = clusterData.slaves.map(node => `
      <div class="cluster-node slave">
        <div class="node-title">Slave Node ${node.node_id}</div>
        <div class="node-stats">
          <div>Files: ${node.files}</div>
          <div>Chunks: ${node.chunks}</div>
          <div>Status: ${node.status}</div>
          <div>Last Sync: ${new Date(node.last_sync).toLocaleTimeString()}</div>
        </div>
        <div class="status-indicator ${node.status === 'active' ? 'healthy' : 'unhealthy'}"></div>
      </div>
    `).join('');

    clusterGrid.innerHTML = masterNode + slaveNodes;
  } catch (error) {
    console.error('Error loading cluster nodes:', error);
    // Fallback to mock data
    const clusterGrid = document.getElementById('production-clusterGrid');
    clusterGrid.innerHTML = `
      <div class="cluster-node master">
        <div class="node-title">Master Node</div>
        <div class="node-stats">
          <div>Files: 15</div><div>Chunks: 45</div><div>Status: healthy</div><div>Heartbeat: Active</div>
        </div>
        <div class="status-indicator healthy"></div>
      </div>
      <div class="cluster-node slave">
        <div class="node-title">Slave Node 01</div>
        <div class="node-stats">
          <div>Files: 15</div><div>Chunks: 45</div><div>Status: healthy</div><div>Heartbeat: Active</div>
        </div>
        <div class="status-indicator healthy"></div>
      </div>
    `;
  }
}

async function loadReplicationLogs() {
  try {
    const response = await fetch(`${apiBases.production}/logs`);
    const logs = await response.json();

    const logsContainer = document.getElementById('production-logs');
    logsContainer.innerHTML = logs.slice(0, 10).map(log => `
      <div class="log-entry ${log.type}">
        <span class="log-timestamp">${new Date(log.timestamp).toLocaleString()}</span> | ${log.message}
      </div>
    `).join('');

    // Auto-scroll to bottom
    logsContainer.scrollTop = logsContainer.scrollHeight;
  } catch (error) {
    console.error('Error loading replication logs:', error);
    // Fallback mock logs
    const logsContainer = document.getElementById('production-logs');
    const mockLogs = [
      { timestamp: new Date().toISOString(), type: 'replication', message: 'File chunk replicated to slave-01' },
      { timestamp: new Date(Date.now() - 15000).toISOString(), type: 'success', message: 'Master-slave sync completed' },
      { timestamp: new Date(Date.now() - 30000).toISOString(), type: 'replication', message: 'File chunk replicated to slave-02' },
      { timestamp: new Date(Date.now() - 45000).toISOString(), type: 'replication', message: 'File chunk replicated to slave-03' }
    ];

    logsContainer.innerHTML = mockLogs.map(log => `
      <div class="log-entry ${log.type}">
        <span class="log-timestamp">${new Date(log.timestamp).toLocaleString()}</span> | ${log.message}
      </div>
    `).join('');
  }
}

// Secure Mode Functions
function switchAuthForm() {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const switchBtn = document.querySelector('.switch-auth-btn');

  if (loginForm.classList.contains('active')) {
    loginForm.classList.remove('active');
    registerForm.classList.add('active');
    switchBtn.textContent = 'Switch to Login';
  } else {
    registerForm.classList.remove('active');
    loginForm.classList.add('active');
    switchBtn.textContent = 'Switch to Register';
  }
}

async function login() {
  const username = document.getElementById('secure-username').value;
  const password = document.getElementById('secure-password').value;

  if (!username || !password) {
    showNotification('Please fill in all fields', 'error');
    return;
  }

  try {
    // Mock authentication - replace with actual API call
    const response = await fetch(`${apiBases.secure}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (response.ok) {
      const data = await response.json();
      currentUser = data.user;
      isLoggedIn = true;

      document.getElementById('auth-panel').style.display = 'none';
      document.getElementById('secure-content').style.display = 'block';

      if (data.user.is_admin) {
        document.getElementById('admin-panel').style.display = 'block';
      }

      loadSecureData();
      showNotification('Login successful', 'success');
    } else {
      showNotification('Invalid credentials', 'error');
    }
  } catch (error) {
    showNotification('Login failed: ' + error.message, 'error');
  }
}

async function register() {
  const username = document.getElementById('register-username').value;
  const password = document.getElementById('register-password').value;
  const confirmPassword = document.getElementById('register-confirm').value;
  const isAdmin = document.getElementById('is-admin').checked;

  if (!username || !password || !confirmPassword) {
    showNotification('Please fill in all fields', 'error');
    return;
  }

  if (password !== confirmPassword) {
    showNotification('Passwords do not match', 'error');
    return;
  }

  try {
    // Mock registration - replace with actual API call
    const response = await fetch(`${apiBases.secure}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, is_admin: isAdmin })
    });

    if (response.ok) {
      showNotification('Registration successful! Please login.', 'success');
      switchAuthForm();
    } else {
      const error = await response.json();
      showNotification('Registration failed: ' + error.message, 'error');
    }
  } catch (error) {
    showNotification('Registration failed: ' + error.message, 'error');
  }
}

async function loadSecureData() {
  // Mock secure data - replace with actual API calls
  document.getElementById('secure-encryptionStatus').textContent = 'Active';
  document.getElementById('secure-usersOnline').textContent = '3';
  document.getElementById('secure-filesStored').textContent = '15';

  // Load secure files
  loadFiles('secure');
}

// Upload Zone Initialization
function initializeUploadZones() {
  const uploadZones = document.querySelectorAll('.upload-zone');

  uploadZones.forEach(zone => {
    const fileInput = zone.querySelector('input[type="file"]');

    zone.addEventListener('click', () => fileInput.click());

    zone.addEventListener('dragover', (e) => {
      e.preventDefault();
      zone.classList.add('dragover');
    });

    zone.addEventListener('dragleave', () => {
      zone.classList.remove('dragover');
    });

    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      zone.classList.remove('dragover');

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        fileInput.files = files;
        // Trigger upload for secure mode
        uploadFile('secure');
      }
    });

    fileInput.addEventListener('change', () => {
      uploadFile('secure');
    });
  });
}

// Utility Functions
function downloadFile(fileId, filename, mode) {
  window.open(`${apiBases[mode]}/download/${fileId}`, '_blank');
}

function showNotification(message, type = 'info') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <span class="notification-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
      <span class="notification-text">${message}</span>
    </div>
  `;

  // Style notification
  notification.style.cssText = `
    position: fixed;
    top: 100px;
    right: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 15px 20px;
    color: white;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    z-index: 10000;
    animation: slideInRight 0.5s ease;
    max-width: 300px;
  `;

  document.body.appendChild(notification);

  // Auto remove after 5 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOutRight 0.5s ease';
    setTimeout(() => notification.remove(), 500);
  }, 5000);
}

// Particle Effects
function createParticles() {
  const canvas = document.createElement('canvas');
  canvas.id = 'particle-canvas';
  canvas.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
  `;
  document.body.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  let particles = [];

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function createParticle(x, y) {
    return {
      x: x || Math.random() * canvas.width,
      y: y || Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2,
      size: Math.random() * 3 + 1,
      opacity: Math.random() * 0.5 + 0.2
    };
  }

  function initParticles() {
    particles = [];
    const particleCount = Math.floor((canvas.width * canvas.height) / 12000);
    for (let i = 0; i < particleCount; i++) {
      particles.push(createParticle());
    }
  }

  function updateParticles() {
    particles.forEach(particle => {
      particle.x += particle.vx;
      particle.y += particle.vy;

      if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
      if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;
    });
  }

  function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(particle => {
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${particle.opacity})`;
      ctx.fill();
    });
  }

  function animate() {
    updateParticles();
    drawParticles();
    requestAnimationFrame(animate);
  }

  resizeCanvas();
  initParticles();
  animate();

  window.addEventListener('resize', () => {
    resizeCanvas();
    initParticles();
  });
}

function createUploadParticles() {
  const canvas = document.getElementById('particle-canvas');
  const ctx = canvas.getContext('2d');

  for (let i = 0; i < 20; i++) {
    setTimeout(() => {
      const particle = {
        x: Math.random() * canvas.width,
        y: canvas.height,
        vy: -Math.random() * 5 - 2,
        vx: (Math.random() - 0.5) * 4,
        size: Math.random() * 4 + 2,
        opacity: 1,
        color: modeThemes[currentMode].accent
      };

      function updateParticle() {
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.vy += 0.1;
        particle.opacity -= 0.02;

        if (particle.opacity > 0) {
          ctx.beginPath();
          ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
          ctx.fillStyle = `${particle.color}${Math.floor(particle.opacity * 255).toString(16).padStart(2, '0')}`;
          ctx.fill();
          requestAnimationFrame(updateParticle);
        }
      }

      updateParticle();
    }, i * 100);
  }
}

// Auto-refresh data every 30 seconds
setInterval(() => {
  if (currentMode !== 'secure' || isLoggedIn) {
    loadModeData(currentMode);
  }
}, 30000);

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.metaKey) {
    switch (e.key) {
      case '1':
        e.preventDefault();
        switchMode('simple');
        break;
      case '2':
        e.preventDefault();
        switchMode('distributed');
        break;
      case '3':
        e.preventDefault();
        switchMode('production');
        break;
      case '4':
        e.preventDefault();
        switchMode('secure');
        break;
    }
  }
});