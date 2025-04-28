import { todos } from '$lib/api';

import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';

export const actions: Actions = {
	remove: async (event) => {
		const id = parseInt(event.params.id);
		const todo = await todos.delete_(id);
		if (todo) {
			redirect(302, '/');
		} else {
			return fail(400, { message: 'Failed to remove a todo' });
		}
	},
	update: async (event) => {
		const id = parseInt(event.params.id);
		const data = await event.request.formData();
		const done = data.get('done');
		const title = data.get('title');
		const payload = {
			done: done ? done === 'on' : false,
			title: title ? title.toString() : undefined
		};
		const todo = await todos.patch(id, payload);
		if (todo) {
			redirect(302, '/');
		} else {
			return fail(400, { message: 'Failed to update a todo' });
		}
	}
};
