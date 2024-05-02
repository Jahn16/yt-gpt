<script lang="ts">
	import Message from '../components/Message.svelte';
	import type { PageServerData } from './$types';

	export let data: PageServerData;
</script>

<div class=".container">
	<div class="row row-cols-1 row-cols-md-1 g-4">
		{#each data.chat as message}
			<Message {message} />{/each}
	</div>
	<div id="chat-form" style="margin-top: 10px;">
		<form method="POST">
			<div class="input-group mb-3">
				<input
					name="message"
					type="text"
					class="form-control"
					placeholder="Enter your message"
					aria-label="Enter your message"
					aria-describedby="button-addon2"
				/>
				<button class="btn btn-primary" type="submit" id="button-addon2"
					>Submit <i class="bi bi-send-fill"></i></button
				>
			</div>
		</form>
	</div>
</div>

<style>
  #chat-form {
		margin: auto;
		width: 60%;
	}
</style>
