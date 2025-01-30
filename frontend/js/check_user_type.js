export async function get_user_type(response){
    if (!response)
        return null
    const user = response.user
    if (!user)
        return null
    return user.type
}