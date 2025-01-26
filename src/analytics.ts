import Analytics from './Analytics.svelte';

const analyticsApp = new Analytics({
  target: document.getElementById('analytics-root')!,
});

export default analyticsApp;
