
const robot = require('robotjs');
const fs = require('fs');
const path = require('path');
const schedule = require('node-schedule');
const { format, addHours } = require('date-fns');

{
    const defaultConfig = {
        failsafeEnabled: true,
        pauseBetweenActions: 100, 
        screenshotEnabled: true,
        logEnabled: true,
        maxRetries: 3
    };

    class AutomationStep {
        constructor(name, action, args = {}) {
            this.name = name;
            this.action = action;
            this.args = args;
            this.id = `step_${Date.now()}`;
        }
    }

    class APIAutomationBot {
        constructor(config = {}) {
            this.config = { ...defaultConfig, ...config };
            this.logDir = path.join(process.cwd(), 'logs', 'automation');
        }

        async typeText(text, interval = 50) {
            if (!text) return;
            if (interval > 0) {
                for (const char of text) {
                    robot.keyTap(char);
                    await new Promise(r => setTimeout(r, interval));
                }
            } else {
                robot.typeString(text);
            }
        }

        async runFullTest(apiName) {
            console.log(`[AUTO] Iniciando teste para ${apiName}`);
            robot.moveMouse(100, 100);
            await this.typeText(`test_api ${apiName}\n`, 30);
            return { success: true, timestamp: new Date() };
        }
    }

    module.exports = { APIAutomationBot, AutomationStep };
}
