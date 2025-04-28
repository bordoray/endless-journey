<script lang="ts">
	let { data } = $props();
</script>

<div class="p-2">
	<h2 class="text-lg font-bold">My TODOs</h2>
	{#if data.todos === null}
		error
	{:else}
		<div class="flex flex-col gap-2 p-2">
			{#each data.todos as todo}
				<form method="POST" class="flex gap-2">
					<input type="checkbox" name="done" checked={todo.done} />
					<input
						class="rounded-md border border-gray-400 p-1"
						type="text"
						name="title"
						value={todo.title}
					/>
					<button
						class="rounded-md bg-blue-600 p-1 text-white"
						formaction="/todos/{todo.id}?/update">更新</button
					>
					<button class="rounded-md bg-red-400 p-1 text-white" formaction="/todos/{todo.id}?/remove"
						>削除</button
					>
				</form>
			{/each}
		</div>
	{/if}
	<div class="mt-4">
		<div>新規作成</div>
		<form method="POST" class="flex gap-2">
			<input class="rounded-md border border-gray-400 p-1" type="text" name="title" />
			<button class="rounded-md bg-green-800 p-1 text-white" formaction="?/add">作成</button>
		</form>
	</div>
</div>
