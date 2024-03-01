import { SnackBar } from "./model";



async function handleResponse(response: Response) : Promise<SnackBar> {
  try {
    return await response.json()
  } catch (error) {
    console.error(error)
    // alert('發生了預期外的錯誤，請檢查網路連線')
    return {status: 'error', message: '發生了預期外的錯誤，請檢查網路連線'}
  }
}

export async function fetch_api(path: string = "") {
  const response = await fetch(`/api${path}`, {
    method: "GET",
    credentials: "include",
  });
  return await handleResponse(response);
}

export async function post_api(path: string = "", data: object | null = null) {
  const response = await fetch(`/api${path}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    credentials: "include",
  });
  return await handleResponse(response);
}

export async function raw_post_api(path: string = "", data: FormData) {
  const response = await fetch(`/api${path}`, {
    method: "POST",
    // headers: {
    //   Accept: "application/json",
    //   // "Content-Type": "application/json",
    //   "Content-Type": "multipart/form-data",
    //   // "boundary":"----WebKitFormBoundary7MA4YWxkTrZu0gW"
    // },
    body: data,
    credentials: "include",
  });
  return await handleResponse(response);
}



export async function patch_api(path: string = "", data: object) {
  const response = await fetch(`/api${path}`, {
    method: "PATCH",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    credentials: "include",
  });
  return await handleResponse(response);
}

export async function delete_api(path: string = "") {
  const response = await fetch(`/api${path}`, {
    method: "DELETE",
    credentials: "include",
  });
  return await handleResponse(response);
}

// export function handleErrorSnackbar(res: {
//   status: NonNullable<"success" | "error" | "info" | "warning">;
//   message: string;
//   data: object | any;
// }) {
//   const store = useAppStore();
//   if (res.status === "success") {
//     return res.data;
//   } else {
//     store.addSnackbar(res);
//     return undefined;
//   }
// }
