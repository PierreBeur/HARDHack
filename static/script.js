const main = document.querySelector('main');

const time = main.querySelector('#time');

function setTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    time.textContent = `${timeString}`;
}

setInterval(setTime, 1000);

const stopwatch = main.querySelector('#stopwatch');
const button = main.querySelector('button');
const buttonImg = button.querySelector('img');

let startTime, elapsedTime = 0.0, timerInterval;

button.addEventListener('click', async () => {
    if (buttonImg.src.includes('start')) { // start
        buttonImg.src = 'static/reset.png';
        button.style.background = 'red';
        startTime = Date.now() - elapsedTime;
        timerInterval = setInterval(() => {
            elapsedTime = Date.now() - startTime;
            const timeString = new Date(elapsedTime).toLocaleTimeString(undefined, {
                minute: "2-digit",
                second: "2-digit",
                fractionalSecondDigits: 2,
            });
            stopwatch.textContent = timeString;
        }, 16);
    } else { // reset
        await fetch('/reset');
        await setData();
        buttonImg.src = 'static/start.png';
        button.style.background = 'greenyellow';
        clearInterval(timerInterval);
        elapsedTime = 0;
        stopwatch.textContent = '00:00.00';
    }
});

const acceleration = main.querySelector('#acceleration');
const gyro = main.querySelector('#gyro');
const speed = main.querySelector('#speed');
const distance = main.querySelector('#distance');
const calories = main.querySelector('#calories');
const temperature = main.querySelector('#temperature');

async function setData() {
    const response = await fetch('/data');
    const json = await response.json();
    const a = json['acceleration'];
    const g = json['gyro'];
    const s = json['speed'];
    const d = json['distance'];
    const t = json['temperature'];
    if (a) {
        // acceleration.textContent = `Acceleration: (${a.x}, ${a.y}, ${a.z})`;
    }
    if (g) {
        // gyro.textContent = `Gyro: (${g.x}, ${g.y}, ${g.z})`;
    }
    if (s) {
        speed.textContent = Math.round(s);
    }
    if (d) {
        distance.textContent = Math.round(d);
        calories.textContent = Math.round(d * 0.062);
    }
    if (t) {
        temperature.textContent = t;
    }
}
setInterval(setData, 500);
