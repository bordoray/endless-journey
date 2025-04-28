import { BACKEND_URL } from '$env/static/private';

type Todo = {
	id: number;
	title: string;
	done: boolean;
	createAt: string;
	updateAt: string;
};

async function get(options: { page?: number } = {}) {
	const url = new URL(`${BACKEND_URL}/todos`);
	const params = new URLSearchParams();
	if (options.page) {
		params.append('page', options.page.toString());
	}
	url.search = params.toString();

	let res: Response;
	try {
		res = await fetch(url.toString());
	} catch (error) {
		console.error(error);
		return null;
	}

	if (!res.ok) {
		console.error(res);
		return null;
	}

	return res.json() as Promise<Todo[]>;
}

async function post(todo: Pick<Todo, 'title'>) {
	const url = `${BACKEND_URL}/todos`;

	let res: Response;
	try {
		res = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(todo)
		});
	} catch (error) {
		console.error(error);
		return null;
	}

	if (!res.ok) {
		console.error(res);
		return null;
	}

	return res.json() as Promise<Todo>;
}

async function delete_(id: number) {
	const url = `${BACKEND_URL}/todos/${id}`;

	let res: Response;
	try {
		res = await fetch(url, {
			method: 'DELETE'
		});
	} catch (error) {
		console.error(error);
		return null;
	}

	if (!res.ok) {
		console.error(res);
		return null;
	}

	return true;
}

async function patch(id: number, todo: Partial<Pick<Todo, 'title' | 'done'>>) {
	const url = `${BACKEND_URL}/todos/${id}`;

	let res: Response;
	try {
		res = await fetch(url, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(todo)
		});
	} catch (error) {
		console.error(error);
		return null;
	}

	if (!res.ok) {
		console.error(res);
		return null;
	}

	return res.json() as Promise<Todo>;
}

export { get, post, delete_, patch };
