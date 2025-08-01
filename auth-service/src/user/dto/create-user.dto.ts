import { IsBoolean, IsNotEmpty, IsOptional, IsString, MaxLength, MinLength } from "class-validator";

export class CreateUserDto{
    @IsString()
    @IsNotEmpty()
    @MaxLength(50)
    telegramId: string;

    @IsString()
    @IsNotEmpty()
    @MaxLength(50)
    username: string;

    @IsString()
    @IsNotEmpty()
    @MinLength(6)
    password: string;

    @IsString()
    @IsOptional()
    @MaxLength(255)
    email?: string;

    @IsBoolean()
    @IsOptional()
    isActive?: boolean;
}