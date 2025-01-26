declare module '*.svelte' {
    import { SvelteComponentTyped } from 'svelte';
    export default class extends SvelteComponentTyped<
      Record<string, any>,
      Record<string, any>,
      Record<string, any>
    > {}
  }