<script lang="ts">
    export let navItems: { name: string; link: string; icon?: string }[] = [];
  </script>
  
  <div class="navbar">
    <div class="navbar-content">
      {#each navItems as navItem}
        <a href={navItem.link} class="navbar-item">
          {#if navItem.icon === 'home'}
            <!-- Inline SVG for home -->
            <svg class="navbar-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 9l9-7 9 7v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
          {:else if navItem.icon === 'chart'}
            <!-- Inline SVG for chart -->
            <svg class="navbar-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 17v2a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-2"></path>
              <path d="M12 6v13"></path>
              <path d="M9 9l3-3 3 3"></path>
            </svg>
          {/if}
          <span>{navItem.name}</span>
        </a>
      {/each}
    </div>
  </div>
  
  <style>
    .navbar {
      position: fixed;
      top: 20px; /* Adjusted to make it lower */
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      background-color: #ffffff; /* Light mode background */
      padding: 1rem 3rem; /* Increased the width */
      border-radius: 15px; /* Less rounded */
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
  
    .navbar-content {
      display: flex;
      gap: 2rem;
      align-items: center;
    }
  
    .navbar-item {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #333; /* Light mode text color */
      text-decoration: none;
      font-size: 16px;
    }
  
    .navbar-item:hover {
      color: #96D291; /* Hover color */
    }
  
    .navbar-icon {
      width: 20px;
      height: 20px;
      color: #333; /* Light mode icon color */
    }
  
    .navbar-item span {
      display: none; /* Hide the name on small screens */
    }
  
    @media (min-width: 768px) {
      .navbar-item span {
        display: inline; /* Show the name on larger screens */
      }
    }
  </style>
  