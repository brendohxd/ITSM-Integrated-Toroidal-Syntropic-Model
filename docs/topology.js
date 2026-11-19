/* Coordinate demonstration only: no field dynamics or physical trajectory. */
(() => {
  const root = document.querySelector('[data-topology-explorer]');
  if (!root) return;
  const slider = root.querySelector('input[type=range]');
  const buttons = [...root.querySelectorAll('[data-axis]')];
  const dot = root.querySelector('[data-periodic-point]');
  const partner = root.querySelector('[data-periodic-partner]');
  const path = root.querySelector('[data-periodic-path]');
  const output = root.querySelector('output');
  const status = root.querySelector('[data-periodic-status]');
  const boundary = root.querySelector('[data-show-boundary]');
  const specs = {
    x: {start:[0,.45,.45], end:[1,.45,.45], color:'#72d7cd'},
    y: {start:[.55,0,.62], end:[.55,1,.62], color:'#e6ba7b'},
    z: {start:[.32,.68,0], end:[.32,.68,1], color:'#b7a0eb'}
  };
  let axis = 'x';
  const project = ([x,y,z]) => [340+170*x-150*y,300+82*x+93*y-200*z];
  function render() {
    const spec = specs[axis];
    const raw = Number(slider.value)/100;
    const fraction = raw === 1 ? 0 : raw;
    const value = spec.start.map((v,i) => v+(spec.end[i]-v)*fraction);
    const [x,y] = project(value);
    const [sx,sy] = project(spec.start);
    const [ex,ey] = project(spec.end);
    dot.setAttribute('cx',x); dot.setAttribute('cy',y); dot.setAttribute('fill',spec.color);
    partner.setAttribute('cx',ex); partner.setAttribute('cy',ey); partner.setAttribute('stroke',spec.color);
    partner.setAttribute('visibility',raw === 1 ? 'visible' : 'hidden');
    path.setAttribute('d',`M ${sx} ${sy} L ${ex} ${ey}`); path.setAttribute('stroke',spec.color);
    root.style.setProperty('--axis-color',spec.color);
    buttons.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.axis === axis)));
    output.textContent = `${axis}/L${axis} = ${fraction.toFixed(2)}`;
    slider.setAttribute('aria-valuetext',raw === 1 ? `${axis} equals 1 and 0 at the identified boundary` : `${axis} fraction ${fraction.toFixed(2)}`);
    status.textContent = raw === 1
      ? `The two highlighted endpoints are the same location under the ${axis} identification. The other two coordinates stay fixed.`
      : `Move along ${axis} while holding the other two coordinates fixed. At the far face, the coordinate continues from its paired face.`;
    boundary.textContent = raw === 1 ? 'Return to the interior' : 'Show the identified boundary';
  }
  buttons.forEach(button => button.addEventListener('click',() => {axis=button.dataset.axis;slider.value='35';render();}));
  slider.addEventListener('input',render);
  boundary.addEventListener('click',() => {slider.value=Number(slider.value) === 100 ? '35' : '100';render();});
  root.querySelector('[data-topology-controls]').hidden=false;
  render();
})();
