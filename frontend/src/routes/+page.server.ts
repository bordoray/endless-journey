import type { PageServerLoad } from './$types';
import { todos } from '$lib/api';

export const load: PageServerLoad = async () => {
	const _todos = await todos.get();

	return {
		todos: _todos
	};
};

import type { Actions } from './$types';
import { fail } from '@sveltejs/kit';

export const actions: Actions = {
	add: async (event) => {
		const data = await event.request.formData();
		const title = data.get('title') as string;
		const todo = await todos.post({ title });
		if (todo) {
			return { success: true };
		} else {
			return fail(400, { message: 'Failed to add a todo' });
		}
	}
};
