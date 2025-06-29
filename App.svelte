<script lang="ts">
  import { push, pop, replace } from 'svelte-spa-router';
  import { onMount } from 'svelte';
  import Router, { type RouterEvent, type RouteDetailLoaded } from 'svelte-spa-router'
  import ComponentA from './ComponentA.svelte';
  import ComponentB from './ComponentB.svelte';
  import ComponentC from './ComponentC.svelte';
  import ComponentD from './ComponentD.svelte';

  type TopSelector = 'option1' | 'option2';
  type BottomSelector = 'optionA' | 'optionB';

  let topSelector: TopSelector = 'option1';
  let bottomSelector: BottomSelector = 'optionA';
  let isInitialized = false;
  let currentComponent: any = null; // デバッグ用

  console.log('Components loaded:', { ComponentA, ComponentB, ComponentC, ComponentD });

  // ルート定義 - デバッグ用のコンソール出力を追加
  const routes = {
    '/': ComponentA,
    '/option1/optionA': ComponentA,
    '/option1/optionB': ComponentB,
    '/option2/optionA': ComponentC,
    '/option2/optionB': ComponentD,
  };

  console.log('Routes defined:', routes);

  // ラジオセレクタの値をURLパスから設定
  function setSelectorsFromPath(path: string): void {
    console.log('Setting selectors from path:', path);
    const parts = path.split('/').filter(p => p);
    if (parts.length >= 2) {
      const [top, bottom] = parts;
      if (isValidCombination(top, bottom)) {
        topSelector = top as TopSelector;
        bottomSelector = bottom as BottomSelector;
        console.log('Selectors updated:', { topSelector, bottomSelector });
      }
    } else {
      // デフォルト値
      topSelector = 'option1';
      bottomSelector = 'optionA';
      console.log('Using default selectors:', { topSelector, bottomSelector });
    }
  }

  // 有効な組み合わせかチェック
  function isValidCombination(top: string, bottom: string): boolean {
    const validTops: TopSelector[] = ['option1', 'option2'];
    const validBottoms: BottomSelector[] = ['optionA', 'optionB'];
    const isValid = validTops.includes(top as TopSelector) && validBottoms.includes(bottom as BottomSelector);
    console.log('Combination validation:', { top, bottom, isValid });
    return isValid;
  }

  // ラジオセレクタの変更時にルートを更新
  function updateRoute(): void {
    if (!isInitialized) {
      console.log('Skipping route update - not initialized');
      return;
    }

    const newPath = `/${topSelector}/${bottomSelector}`;
    console.log('Updating route to:', newPath);
    push(newPath);
  }

  // ルート変更イベントをリッスン
  function handleRouteLoaded(event: RouterEvent<RouteDetailLoaded>): void {
    console.log('Route loaded event:', event.detail);
    const path: string = event.detail.location;
    currentComponent = event.detail.component; // デバッグ用
    console.log('Current component set to:', currentComponent);

    // 一時的にフラグを無効化してリアクティブ文による更新を防ぐ
    isInitialized = false;
    setSelectorsFromPath(path);
    isInitialized = true;
  }

  // ラジオボタンの変更ハンドラ
  function handleTopSelectorChange(): void {
    console.log('Top selector changed to:', topSelector);
    updateRoute();
  }

  function handleBottomSelectorChange(): void {
    console.log('Bottom selector changed to:', bottomSelector);
    updateRoute();
  }

  onMount(() => {
    console.log('Component mounted');

    // 初期パスの設定
    const currentPath = window.location.hash.slice(1) || '/';
    console.log('Current path on mount:', currentPath);

    setSelectorsFromPath(currentPath);

    // 初期パスが空の場合はデフォルトルートに移動
    if (currentPath === '/') {
      console.log('Redirecting to default route');
      replace('/option1/optionA');
    }

    // 初期化完了
    isInitialized = true;
    console.log('Initialization completed');
  });
</script>

<div>
  <!-- ラジオボタン群 -->
  <div class="mb-4">
    <h3>Top Selector:</h3>
    <label>
      <input
        type="radio"
        bind:group={topSelector}
        value="option1"
        on:change={handleTopSelectorChange}
      />
      Option 1
    </label>
    <label>
      <input
        type="radio"
        bind:group={topSelector}
        value="option2"
        on:change={handleTopSelectorChange}
      />
      Option 2
    </label>
  </div>

  <div class="mb-4">
    <h3>Bottom Selector:</h3>
    <label>
      <input
        type="radio"
        bind:group={bottomSelector}
        value="optionA"
        on:change={handleBottomSelectorChange}
      />
      Option A
    </label>
    <label>
      <input
        type="radio"
        bind:group={bottomSelector}
        value="optionB"
        on:change={handleBottomSelectorChange}
      />
      Option B
    </label>
  </div>

  <!-- 現在の選択状態を表示（デバッグ用） -->
  <div class="mb-4 p-2 bg-gray-100">
    <p>Current selection: {topSelector} / {bottomSelector}</p>
    <p>Current path: /{topSelector}/{bottomSelector}</p>
    <p>Current component: {currentComponent ? currentComponent.name || 'Component loaded' : 'None'}</p>
    <p>Window hash: {typeof window !== 'undefined' ? window.location.hash : 'N/A'}</p>
  </div>

  <!-- ComponentCが読み込まれているかテスト -->
  <div class="mb-4 p-2 bg-yellow-100">
    <h4>Component Test (should show ComponentC):</h4>
    <ComponentC />
  </div>

  <!-- ルーターコンポーネント -->
  <div class="bg-white rounded-lg shadow-lg border-2 border-blue-200 min-h-[300px] p-4">
    <h4>Router Content:</h4>
    <Router
      {routes}
      on:routeLoaded={handleRouteLoaded}
    />
  </div>
</div>

<style>
  label {
    display: block;
    margin: 0.5rem 0;
  }

  input[type="radio"] {
    margin-right: 0.5rem;
  }
</style>
