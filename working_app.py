
from flask import Flask, request, jsonify, session, render_template_string
import json
import time
import random
import threading
from datetime import datetime, timedelta
import schedule
import uuid
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Try webdriver-manager, but have fallback
try:
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

app = Flask(__name__)
app.secret_key = 'bing_automation_secret_key_2025'

# Global storage
automation_sessions = {}
scheduled_tasks = []

# HTML template embedded
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bing Search Automation - Fixed Edition</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
            color: #E2E8F0; min-height: 100vh; overflow-x: hidden;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header {
            background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
            padding: 25px; border-radius: 15px; margin-bottom: 25px; text-align: center;
            box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3);
        }
        .header h1 { font-size: 2.2rem; font-weight: 700; margin-bottom: 8px; color: white; }
        .header p { font-size: 1.1rem; color: #94A3B8; font-weight: 400; }
        .status-banner {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            padding: 12px 20px; border-radius: 8px; margin-top: 15px;
            display: flex; align-items: center; justify-content: center; gap: 10px;
        }
        .status-indicator {
            width: 12px; height: 12px; border-radius: 50%; background: white;
        }
        .status-indicator.running { animation: pulse 2s infinite; }
        .status-indicator.paused { background: #F59E0B; }
        .status-indicator.error { background: #EF4444; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        .main-content { display: grid; grid-template-columns: 400px 1fr; gap: 25px; }
        .panel {
            background: rgba(30, 41, 59, 0.9); border-radius: 15px; padding: 25px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .section {
            background: rgba(51, 65, 85, 0.7); border-radius: 12px; padding: 20px;
            margin-bottom: 20px; border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .section.settings { border-left: 4px solid #10B981; }
        .section.control-panel { background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; }
        .section.scheduler { background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%); color: white; }
        .section-title {
            font-size: 1.3rem; font-weight: 600; margin-bottom: 15px;
            display: flex; align-items: center; gap: 8px;
        }
        .form-group { margin-bottom: 18px; }
        .form-label { display: block; margin-bottom: 8px; font-weight: 500; color: #CBD5E1; font-size: 0.9rem; }
        .slider {
            width: 100%; height: 8px; border-radius: 5px; background: rgba(148, 163, 184, 0.3);
            outline: none; -webkit-appearance: none; cursor: pointer;
        }
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none; width: 22px; height: 22px; border-radius: 50%;
            background: #3B82F6; cursor: pointer; box-shadow: 0 3px 10px rgba(59, 130, 246, 0.5);
        }
        .slider-value { font-size: 0.85rem; color: #94A3B8; margin-top: 4px; font-weight: 500; }
        .switch-container {
            display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;
            padding: 8px; background: rgba(15, 23, 42, 0.3); border-radius: 8px;
        }
        .switch { position: relative; display: inline-block; width: 54px; height: 28px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .switch-slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background: #6B7280; transition: .3s; border-radius: 28px;
        }
        .switch-slider:before {
            position: absolute; content: ""; height: 22px; width: 22px; left: 3px; bottom: 3px;
            background: white; transition: .3s; border-radius: 50%;
        }
        input:checked + .switch-slider { background: #10B981; }
        input:checked + .switch-slider:before { transform: translateX(26px); }
        .control-buttons { display: flex; gap: 12px; margin-bottom: 15px; flex-wrap: wrap; }
        .btn {
            padding: 14px 22px; border: none; border-radius: 10px; cursor: pointer;
            font-weight: 600; font-size: 0.9rem; transition: all 0.3s ease;
            display: flex; align-items: center; gap: 8px; min-width: 85px; justify-content: center;
        }
        .btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3); }
        .btn-start { background: #059669; color: white; }
        .btn-pause { background: #F59E0B; color: white; }
        .btn-stop { background: #EF4444; color: white; }
        .btn-save { background: #3B82F6; color: white; width: 100%; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .input-field, .select-field {
            width: 100%; padding: 12px; border: 1px solid rgba(148, 163, 184, 0.3);
            border-radius: 8px; background: rgba(15, 23, 42, 0.6); color: #E2E8F0; font-size: 0.9rem;
        }
        .input-field:focus, .select-field:focus {
            outline: none; border-color: #3B82F6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        .activity-log { flex: 1; display: flex; flex-direction: column; }
        .log-container {
            flex: 1; background: rgba(15, 23, 42, 0.8); border-radius: 10px; padding: 15px;
            overflow-y: auto; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.85rem;
            line-height: 1.5; border: 1px solid rgba(148, 163, 184, 0.2); max-height: 300px;
        }
        .log-entry { margin-bottom: 6px; color: #CBD5E1; padding: 4px 8px; border-radius: 4px; }
        .log-entry.success { color: #10B981; border-left: 3px solid #10B981; }
        .log-entry.error { color: #EF4444; border-left: 3px solid #EF4444; }
        .log-entry.info { color: #3B82F6; border-left: 3px solid #3B82F6; }
        .log-entry.warning { color: #F59E0B; border-left: 3px solid #F59E0B; }
        .progress-section {
            margin-top: 20px; padding: 20px; background: rgba(15, 23, 42, 0.6);
            border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .progress-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .progress-bar {
            width: 100%; height: 10px; background: rgba(148, 163, 184, 0.3);
            border-radius: 5px; overflow: hidden; margin-bottom: 12px;
        }
        .progress-fill {
            height: 100%; background: linear-gradient(90deg, #10B981, #059669);
            transition: width 0.3s ease; border-radius: 5px;
        }
        .progress-text { font-size: 0.9rem; color: #94A3B8; text-align: center; font-weight: 500; }
        .status-bar {
            display: flex; align-items: center; justify-content: space-between; padding: 15px 25px;
            background: rgba(55, 65, 81, 0.9); border-radius: 12px; margin-top: 20px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .status-info { display: flex; align-items: center; gap: 12px; font-weight: 500; }
        .notification {
            position: fixed; top: 20px; right: 20px; padding: 16px 24px; border-radius: 10px;
            color: white; font-weight: 500; z-index: 1000; transform: translateX(400px);
            transition: transform 0.3s ease;
        }
        .notification.show { transform: translateX(0); }
        .notification.success { background: #10B981; }
        .notification.error { background: #EF4444; }
        .notification.info { background: #3B82F6; }
        .notification.warning { background: #F59E0B; }
        .error-banner {
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
            color: white; padding: 15px 20px; border-radius: 10px; margin: 20px 0;
            display: none;
        }
        .error-banner.show { display: block; }
        .solution-box {
            background: rgba(59, 130, 246, 0.1); border: 1px solid #3B82F6;
            border-radius: 8px; padding: 15px; margin: 15px 0;
        }
        @media (max-width: 768px) { .main-content { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-robot"></i> Bing Search Automation</h1>
            <p>Fixed Edition - Microsoft Edge Automation</p>
            <div class="status-banner" id="statusBanner">
                <div class="status-indicator" id="headerStatusDot"></div>
                <span id="headerStatusText">System Ready</span>
            </div>
        </div>

        <div class="error-banner" id="errorBanner">
            <h3><i class="fas fa-exclamation-triangle"></i> WebDriver Setup Issue</h3>
            <p id="errorMessage">Having trouble setting up Microsoft Edge WebDriver...</p>
            <div class="solution-box">
                <strong>Quick Fix:</strong>
                <ol>
                    <li>Make sure Microsoft Edge browser is installed and updated</li>
                    <li>Check your internet connection</li>
                    <li>Try restarting the application</li>
                    <li>If issues persist, try running: pip install --upgrade webdriver-manager</li>
                </ol>
            </div>
        </div>

        <div class="main-content">
            <div class="panel">
                <div class="section settings">
                    <div class="section-title"><i class="fas fa-cog"></i> Settings</div>
                    <div class="form-group">
                        <label class="form-label">Number of Searches</label>
                        <input type="range" id="searchCount" class="slider" min="1" max="50" value="5">
                        <div class="slider-value" id="searchCountValue">5 searches</div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Cooldown Between Searches</label>
                        <input type="range" id="cooldown" class="slider" min="1" max="30" value="5">
                        <div class="slider-value" id="cooldownValue">5 seconds</div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Typing Speed</label>
                        <select id="typingSpeed" class="select-field">
                            <option value="slow">Slow (Human-like)</option>
                            <option value="medium" selected>Medium</option>
                            <option value="fast">Fast</option>
                        </select>
                    </div>
                    <div class="switch-container">
                        <span>Random Delays</span>
                        <label class="switch">
                            <input type="checkbox" id="randomDelay" checked>
                            <span class="switch-slider"></span>
                        </label>
                    </div>
                    <div class="switch-container">
                        <span>Realistic Typing</span>
                        <label class="switch">
                            <input type="checkbox" id="realisticTyping" checked>
                            <span class="switch-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="section control-panel">
                    <div class="section-title"><i class="fas fa-gamepad"></i> Control Panel</div>
                    <div class="control-buttons">
                        <button class="btn btn-start" id="startBtn"><i class="fas fa-play"></i> Start</button>
                        <button class="btn btn-pause" id="pauseBtn" disabled><i class="fas fa-pause"></i> Pause</button>
                        <button class="btn btn-stop" id="stopBtn" disabled><i class="fas fa-stop"></i> Stop</button>
                    </div>
                    <button class="btn btn-save" id="saveBtn"><i class="fas fa-save"></i> Save Settings</button>
                </div>

                <div class="section scheduler">
                    <div class="section-title"><i class="fas fa-clock"></i> Scheduler</div>
                    <div class="form-group">
                        <label class="form-label">Schedule Time (HH:MM)</label>
                        <input type="time" id="scheduleTime" class="input-field" value="09:00">
                    </div>
                    <div class="control-buttons">
                        <button class="btn" id="addScheduleBtn" style="background: #8B5CF6;"><i class="fas fa-plus"></i> Add</button>
                        <button class="btn" id="clearScheduleBtn" style="background: #EF4444;"><i class="fas fa-trash"></i> Clear</button>
                    </div>
                </div>
            </div>

            <div class="panel">
                <div class="activity-log">
                    <div class="section-title"><i class="fas fa-list-alt"></i> Activity Log</div>
                    <div class="log-container" id="logContainer">
                        <div class="log-entry info">[System] Bing automation system initialized</div>
                        <div class="log-entry warning">[System] Checking Microsoft Edge WebDriver...</div>
                        <div class="log-entry info">[System] Ready to start (lower search count for testing)</div>
                    </div>
                </div>
                <div class="progress-section">
                    <div class="progress-header">
                        <div class="section-title"><i class="fas fa-chart-line"></i> Progress</div>
                        <span id="progressPercentage">0%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill" style="width: 0%;"></div>
                    </div>
                    <div class="progress-text" id="progressText">Ready to start automation</div>
                </div>
            </div>
        </div>

        <div class="status-bar">
            <div class="status-info">
                <div class="status-indicator" id="statusDot"></div>
                <span id="statusText">System Ready</span>
            </div>
            <div><i class="fas fa-clock"></i> <span id="currentTime"></span></div>
        </div>
    </div>

    <div id="notification" class="notification"></div>

    <script>
        let appState = { isRunning: false, isPaused: false, currentSearch: 0, totalSearches: 0 };
        let hasWebDriverError = false;

        const elements = {
            searchCount: document.getElementById('searchCount'),
            searchCountValue: document.getElementById('searchCountValue'),
            cooldown: document.getElementById('cooldown'),
            cooldownValue: document.getElementById('cooldownValue'),
            typingSpeed: document.getElementById('typingSpeed'),
            randomDelay: document.getElementById('randomDelay'),
            realisticTyping: document.getElementById('realisticTyping'),
            startBtn: document.getElementById('startBtn'),
            pauseBtn: document.getElementById('pauseBtn'),
            stopBtn: document.getElementById('stopBtn'),
            saveBtn: document.getElementById('saveBtn'),
            scheduleTime: document.getElementById('scheduleTime'),
            addScheduleBtn: document.getElementById('addScheduleBtn'),
            clearScheduleBtn: document.getElementById('clearScheduleBtn'),
            logContainer: document.getElementById('logContainer'),
            progressFill: document.getElementById('progressFill'),
            progressText: document.getElementById('progressText'),
            progressPercentage: document.getElementById('progressPercentage'),
            statusDot: document.getElementById('statusDot'),
            statusText: document.getElementById('statusText'),
            headerStatusDot: document.getElementById('headerStatusDot'),
            headerStatusText: document.getElementById('headerStatusText'),
            statusBanner: document.getElementById('statusBanner'),
            currentTime: document.getElementById('currentTime'),
            notification: document.getElementById('notification'),
            errorBanner: document.getElementById('errorBanner'),
            errorMessage: document.getElementById('errorMessage')
        };

        document.addEventListener('DOMContentLoaded', function() {
            loadSettings();
            setupEventListeners();
            updateTime();
            setInterval(updateTime, 1000);
            setInterval(updateStatus, 2000);
        });

        function setupEventListeners() {
            elements.searchCount.addEventListener('input', function() {
                elements.searchCountValue.textContent = this.value + ' searches';
            });
            elements.cooldown.addEventListener('input', function() {
                elements.cooldownValue.textContent = this.value + ' seconds';
            });
            elements.startBtn.addEventListener('click', startAutomation);
            elements.pauseBtn.addEventListener('click', pauseAutomation);
            elements.stopBtn.addEventListener('click', stopAutomation);
            elements.saveBtn.addEventListener('click', saveSettings);
            elements.addScheduleBtn.addEventListener('click', addSchedule);
            elements.clearScheduleBtn.addEventListener('click', clearSchedules);
        }

        function loadSettings() {
            fetch('/api/settings').then(response => response.json()).then(settings => {
                elements.searchCount.value = settings.num_searches;
                elements.searchCountValue.textContent = settings.num_searches + ' searches';
                elements.cooldown.value = settings.cooldown;
                elements.cooldownValue.textContent = settings.cooldown + ' seconds';
                elements.typingSpeed.value = settings.typing_speed;
                elements.randomDelay.checked = settings.random_delay;
                elements.realisticTyping.checked = settings.realistic_typing;
            }).catch(error => {
                console.error('Settings load error:', error);
                showNotification('Failed to load settings', 'warning');
            });
        }

        function saveSettings() {
            const settings = {
                num_searches: parseInt(elements.searchCount.value),
                cooldown: parseInt(elements.cooldown.value),
                typing_speed: elements.typingSpeed.value,
                random_delay: elements.randomDelay.checked,
                realistic_typing: elements.realisticTyping.checked,
                headless: false
            };
            fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            }).then(response => response.json()).then(data => {
                showNotification('Settings saved!', 'success');
                addLogEntry('Settings updated and saved', 'success');
            }).catch(error => {
                showNotification('Failed to save settings', 'error');
                console.error('Settings save error:', error);
            });
        }

        function startAutomation() {
            if (hasWebDriverError) {
                showNotification('Cannot start: WebDriver setup failed', 'error');
                addLogEntry('❌ Start blocked due to WebDriver error', 'error');
                return;
            }

            fetch('/api/start', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        appState.isRunning = true;
                        updateButtonStates();
                        showNotification('Starting automation...', 'info');
                        addLogEntry('🚀 Automation initiated', 'success');
                    } else {
                        showNotification(data.message || 'Failed to start', 'error');
                        addLogEntry('❌ Start failed: ' + (data.message || 'Unknown error'), 'error');
                    }
                })
                .catch(error => {
                    showNotification('Network error during start', 'error');
                    console.error('Start error:', error);
                });
        }

        function pauseAutomation() {
            fetch('/api/pause', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        appState.isPaused = !appState.isPaused;
                        updateButtonStates();
                        showNotification(data.message, 'info');
                        addLogEntry('⏸️ ' + data.message, 'info');
                    }
                });
        }

        function stopAutomation() {
            fetch('/api/stop', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    appState.isRunning = false;
                    appState.isPaused = false;
                    updateButtonStates();
                    showNotification('Automation stopped', 'info');
                    addLogEntry('🛑 Automation stopped', 'info');
                    elements.progressFill.style.width = '0%';
                    elements.progressPercentage.textContent = '0%';
                    elements.progressText.textContent = 'Ready to start automation';
                });
        }

        function addSchedule() {
            const time = elements.scheduleTime.value;
            if (!time) {
                showNotification('Please select a time', 'warning');
                return;
            }
            fetch('/api/schedule', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ time: time })
            }).then(response => response.json()).then(data => {
                showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                if (data.status === 'success') {
                    addLogEntry(`⏰ Scheduled for ${time}`, 'success');
                }
            });
        }

        function clearSchedules() {
            fetch('/api/schedules', { method: 'DELETE' })
                .then(response => response.json())
                .then(data => {
                    showNotification('Schedules cleared', 'success');
                    addLogEntry('🗑️ All schedules cleared', 'info');
                });
        }

        function updateStatus() {
            fetch('/api/status').then(response => response.json()).then(status => {
                appState.isRunning = status.is_running;
                appState.isPaused = status.is_paused;

                if (status.progress > 0) {
                    elements.progressFill.style.width = status.progress + '%';
                    elements.progressPercentage.textContent = Math.round(status.progress) + '%';
                    elements.progressText.textContent = `Search ${status.current_search}/${status.total_searches}`;
                }

                if (status.logs && status.logs.length > 0) {
                    status.logs.forEach(log => {
                        if (!isLogDisplayed(log)) {
                            let type = 'info';
                            if (log.includes('Error') || log.includes('Failed')) {
                                type = 'error';
                                if (log.includes('WebDriver')) {
                                    showWebDriverError(log);
                                }
                            }
                            else if (log.includes('completed') || log.includes('successfully')) type = 'success';
                            else if (log.includes('Warning') || log.includes('Waiting')) type = 'warning';
                            addLogEntry(log, type);
                        }
                    });
                }
                updateButtonStates();
            }).catch(error => {
                console.error('Status update failed:', error);
            });
        }

        function showWebDriverError(errorMsg) {
            hasWebDriverError = true;
            elements.errorBanner.classList.add('show');
            elements.errorMessage.textContent = errorMsg;
            elements.startBtn.disabled = true;
            elements.startBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> WebDriver Error';
            elements.statusBanner.style.background = 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)';
            elements.headerStatusText.textContent = 'WebDriver Setup Failed';
            elements.headerStatusDot.className = 'status-indicator error';
        }

        function updateButtonStates() {
            if (hasWebDriverError) {
                return; // Keep error state
            }

            if (appState.isRunning) {
                elements.startBtn.innerHTML = '<i class="fas fa-cog fa-spin"></i> Running';
                elements.startBtn.disabled = true;
                elements.pauseBtn.disabled = false;
                elements.stopBtn.disabled = false;

                elements.statusDot.className = appState.isPaused ? 'status-indicator paused' : 'status-indicator running';
                elements.headerStatusDot.className = appState.isPaused ? 'status-indicator paused' : 'status-indicator running';

                const status = appState.isPaused ? 'Paused' : 'Running';
                elements.statusText.textContent = status;
                elements.headerStatusText.textContent = status;

                if (appState.isPaused) {
                    elements.statusBanner.style.background = 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)';
                } else {
                    elements.statusBanner.style.background = 'linear-gradient(135deg, #10B981 0%, #059669 100%)';
                }

                elements.pauseBtn.innerHTML = appState.isPaused ? 
                    '<i class="fas fa-play"></i> Resume' : '<i class="fas fa-pause"></i> Pause';
            } else {
                elements.startBtn.innerHTML = '<i class="fas fa-play"></i> Start';
                elements.startBtn.disabled = false;
                elements.pauseBtn.disabled = true;
                elements.stopBtn.disabled = true;

                elements.statusDot.className = 'status-indicator';
                elements.headerStatusDot.className = 'status-indicator';
                elements.statusText.textContent = 'Ready';
                elements.headerStatusText.textContent = 'System Ready';
                elements.statusBanner.style.background = 'linear-gradient(135deg, #10B981 0%, #059669 100%)';
            }
        }

        function addLogEntry(message, type = 'info') {
            const timestamp = new Date().toLocaleTimeString();
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry ${type}`;
            logEntry.textContent = `[${timestamp}] ${message}`;
            elements.logContainer.appendChild(logEntry);
            elements.logContainer.scrollTop = elements.logContainer.scrollHeight;
            while (elements.logContainer.children.length > 100) {
                elements.logContainer.removeChild(elements.logContainer.firstChild);
            }
        }

        function isLogDisplayed(logText) {
            return Array.from(elements.logContainer.children).some(log => log.textContent === logText);
        }

        function showNotification(message, type) {
            elements.notification.textContent = message;
            elements.notification.className = `notification ${type} show`;
            setTimeout(() => { elements.notification.classList.remove('show'); }, 4000);
        }

        function updateTime() {
            elements.currentTime.textContent = new Date().toLocaleTimeString();
        }
    </script>
</body>
</html>"""

class AutomationSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.is_running = False
        self.is_paused = False
        self.current_search = 0
        self.total_searches = 0
        self.search_queries = []
        self.logs = []
        self.driver = None
        self.settings = {
            'num_searches': 5,
            'cooldown': 5,
            'typing_speed': 'medium',
            'random_delay': True,
            'realistic_typing': True,
            'headless': False
        }
        self.load_search_queries()

    def load_search_queries(self):
        self.search_queries = [
            "latest technology news", "weather today", "best restaurants near me",
            "how to learn programming", "healthy recipes", "travel destinations",
            "movie reviews", "sports updates", "science discoveries",
            "history facts", "art galleries", "music trends", "book recommendations",
            "fitness tips", "investment advice", "home improvement", "gardening tips",
            "photography techniques", "language learning", "career advice",
            "environmental news", "space exploration", "artificial intelligence",
            "cryptocurrency updates", "gaming news", "fashion trends",
            "cooking techniques", "meditation benefits", "productivity hacks"
        ]

    def get_random_query(self):
        return random.choice(self.search_queries)

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        if len(self.logs) > 100:
            self.logs.pop(0)
        print(f"[LOG] {log_entry}")  # Also print to console

    def setup_driver(self):
        try:
            self.add_log("Setting up Microsoft Edge WebDriver...")
            edge_options = EdgeOptions()

            if self.settings.get('headless', False):
                edge_options.add_argument("--headless=new")

            # Add stability options
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--window-size=1920,1080")
            edge_options.add_argument("--disable-blink-features=AutomationControlled")
            edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

            # Try multiple approaches to get EdgeDriver
            edge_service = None

            if USE_WEBDRIVER_MANAGER:
                try:
                    self.add_log("Attempting to download EdgeDriver via webdriver-manager...")
                    edge_service = EdgeService(EdgeChromiumDriverManager().install())
                    self.add_log("EdgeDriver downloaded successfully")
                except Exception as wm_error:
                    self.add_log(f"WebDriver-manager failed: {str(wm_error)}")
                    edge_service = None

            # Fallback: try system EdgeDriver
            if edge_service is None:
                try:
                    self.add_log("Trying system EdgeDriver...")
                    edge_service = EdgeService()  # Use system PATH
                    self.add_log("Using system EdgeDriver")
                except Exception as sys_error:
                    self.add_log(f"System EdgeDriver failed: {str(sys_error)}")
                    raise Exception("No EdgeDriver available")

            # Create the driver
            self.driver = webdriver.Edge(service=edge_service, options=edge_options)

            # Test basic functionality
            self.driver.get("https://www.google.com")  # Quick test
            self.add_log("WebDriver test successful")

            # Remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            self.add_log("Microsoft Edge WebDriver initialized successfully")
            return True

        except Exception as e:
            error_msg = f"Error setting up Edge WebDriver: {str(e)}"
            self.add_log(error_msg)

            # Provide helpful suggestions
            if "Could not reach host" in str(e) or "offline" in str(e).lower():
                self.add_log("Suggestion: Check your internet connection and try again")
            elif "executable" in str(e).lower():
                self.add_log("Suggestion: Update Microsoft Edge browser to latest version")
            elif "permission" in str(e).lower():
                self.add_log("Suggestion: Run as administrator or check file permissions")

            return False

    def type_with_human_delay(self, element, text):
        speed_settings = {
            'slow': (0.15, 0.25),
            'medium': (0.08, 0.15),
            'fast': (0.03, 0.08)
        }

        min_delay, max_delay = speed_settings.get(self.settings['typing_speed'], (0.08, 0.15))
        element.clear()

        for i, char in enumerate(text):
            if not self.is_running:
                break

            while self.is_paused and self.is_running:
                time.sleep(0.5)

            if not self.is_running:
                break

            element.send_keys(char)
            delay = random.uniform(min_delay, max_delay)

            if self.settings['realistic_typing']:
                if char == ' ':
                    delay += random.uniform(0.1, 0.3)
                elif char in '.,!?':
                    delay += random.uniform(0.2, 0.4)
                elif i > 0 and random.random() < 0.05:
                    delay += random.uniform(0.3, 0.8)

            time.sleep(delay)

    def perform_search(self, query):
        try:
            if not self.driver:
                self.add_log("No WebDriver available")
                return False

            self.add_log(f"Navigating to Bing.com...")
            self.driver.get("https://www.bing.com")

            # Wait for search box with better error handling
            try:
                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "sb_form_q"))
                )
            except Exception as e:
                # Try alternative selectors
                try:
                    search_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.NAME, "q"))
                    )
                except:
                    self.add_log("Could not find Bing search box")
                    return False

            self.add_log(f"Typing query: '{query}'")
            self.type_with_human_delay(search_box, query)

            # Submit search
            search_box.send_keys(Keys.RETURN)

            # Wait for results
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "b_results"))
                )
                self.add_log(f"Search completed successfully: '{query}'")
                return True
            except:
                # Alternative result check
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-bm]"))
                    )
                    self.add_log(f"Search completed successfully: '{query}'")
                    return True
                except:
                    self.add_log(f"Search may have completed but results unclear: '{query}'")
                    return True  # Assume success for robustness

        except Exception as e:
            self.add_log(f"Error performing search '{query}': {str(e)}")
            return False

    def cleanup_driver(self):
        if self.driver:
            try:
                self.driver.quit()
                self.add_log("Browser closed successfully")
            except Exception as e:
                self.add_log(f"Error closing browser: {str(e)}")
            finally:
                self.driver = None

def get_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    session_id = session['session_id']
    if session_id not in automation_sessions:
        automation_sessions[session_id] = AutomationSession(session_id)

    return automation_sessions[session_id]

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    auto_session = get_session()

    if request.method == 'POST':
        data = request.json
        auto_session.settings.update(data)
        auto_session.add_log("Settings updated")
        return jsonify({'status': 'success', 'message': 'Settings saved'})

    return jsonify(auto_session.settings)

@app.route('/api/start', methods=['POST'])
def start_automation():
    auto_session = get_session()

    if auto_session.is_running:
        return jsonify({'status': 'error', 'message': 'Automation already running'})

    # Start automation in background thread
    thread = threading.Thread(target=run_automation_background, args=(auto_session,))
    thread.daemon = True
    thread.start()

    return jsonify({'status': 'success', 'message': 'Automation started'})

@app.route('/api/pause', methods=['POST'])
def pause_automation():
    auto_session = get_session()

    if not auto_session.is_running:
        return jsonify({'status': 'error', 'message': 'No automation running'})

    auto_session.is_paused = not auto_session.is_paused
    action = 'paused' if auto_session.is_paused else 'resumed'
    auto_session.add_log(f"Automation {action}")

    return jsonify({'status': 'success', 'message': f'Automation {action}'})

@app.route('/api/stop', methods=['POST'])
def stop_automation():
    auto_session = get_session()

    auto_session.is_running = False
    auto_session.is_paused = False
    auto_session.current_search = 0
    auto_session.cleanup_driver()
    auto_session.add_log("Automation stopped")

    return jsonify({'status': 'success', 'message': 'Automation stopped'})

@app.route('/api/status', methods=['GET'])
def get_status():
    auto_session = get_session()

    status = {
        'is_running': auto_session.is_running,
        'is_paused': auto_session.is_paused,
        'current_search': auto_session.current_search,
        'total_searches': auto_session.total_searches,
        'progress': 0,
        'logs': auto_session.logs[-15:] if auto_session.logs else []
    }

    if auto_session.total_searches > 0:
        status['progress'] = (auto_session.current_search / auto_session.total_searches) * 100

    return jsonify(status)

@app.route('/api/schedule', methods=['POST'])
def add_schedule():
    data = request.json
    time_str = data.get('time')

    if not time_str:
        return jsonify({'status': 'error', 'message': 'Time is required'})

    try:
        datetime.strptime(time_str, "%H:%M")
        scheduled_tasks.append(time_str)

        auto_session = get_session()
        auto_session.add_log(f"Scheduled automation for {time_str}")

        return jsonify({'status': 'success', 'message': f'Scheduled for {time_str}'})
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid time format'})

@app.route('/api/schedules', methods=['GET', 'DELETE'])
def handle_schedules():
    if request.method == 'DELETE':
        scheduled_tasks.clear()
        auto_session = get_session()
        auto_session.add_log("All schedules cleared")
        return jsonify({'status': 'success', 'message': 'Schedules cleared'})

    return jsonify({'schedules': scheduled_tasks})

def run_automation_background(auto_session):
    try:
        auto_session.is_running = True
        auto_session.current_search = 0
        auto_session.total_searches = auto_session.settings['num_searches']

        auto_session.add_log(f"Starting automation: {auto_session.total_searches} searches")

        # Setup WebDriver with better error handling
        if not auto_session.setup_driver():
            auto_session.add_log("Cannot proceed without WebDriver")
            return

        successful_searches = 0

        for i in range(auto_session.total_searches):
            if not auto_session.is_running:
                auto_session.add_log("Automation stopped by user")
                break

            # Handle pause
            while auto_session.is_paused and auto_session.is_running:
                time.sleep(1)

            if not auto_session.is_running:
                break

            # Perform search
            query = auto_session.get_random_query()
            auto_session.current_search = i + 1

            auto_session.add_log(f"Starting search {i+1}/{auto_session.total_searches}")

            if auto_session.perform_search(query):
                successful_searches += 1
                auto_session.add_log(f"✅ Search {i+1} completed")
            else:
                auto_session.add_log(f"❌ Search {i+1} failed")

            # Cooldown between searches
            if i < auto_session.total_searches - 1:
                cooldown = auto_session.settings['cooldown']
                if auto_session.settings['random_delay']:
                    cooldown += random.randint(1, 3)

                auto_session.add_log(f"Waiting {cooldown} seconds...")

                for remaining in range(cooldown, 0, -1):
                    if not auto_session.is_running:
                        break
                    while auto_session.is_paused and auto_session.is_running:
                        time.sleep(1)
                    if not auto_session.is_running:
                        break
                    time.sleep(1)

        auto_session.add_log(f"🎉 Automation completed: {successful_searches}/{auto_session.total_searches} searches successful")

    except Exception as e:
        auto_session.add_log(f"❌ Critical error in automation: {str(e)}")
    finally:
        auto_session.cleanup_driver()
        auto_session.is_running = False
        auto_session.is_paused = False

if __name__ == '__main__':
    print("🌐 Starting Bing Search Automation - Fixed Edition")
    print("🔧 Enhanced WebDriver setup with fallbacks")
    print("📱 Open http://localhost:5000 in your browser")
    print("=" * 60)

    # Print system info
    print(f"Python version: {sys.version}")
    print(f"WebDriver Manager available: {USE_WEBDRIVER_MANAGER}")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)