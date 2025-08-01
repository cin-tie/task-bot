import { Injectable, UnauthorizedException } from "@nestjs/common";
import { JwtService } from "@nestjs/jwt";
import { UserService } from "src/user/user.service";
import { RegisterDto } from "./dto/register.dto";
import { User } from "src/user/user.entity";
import { LoginDto } from "./dto/login.dto";

@Injectable()
export class AuthService{
    constructor(
        private readonly userService: UserService,
        private readonly jwrService: JwtService,
    ) {}

    async register(registerDto: RegisterDto): Promise<{access_token: string}>{
        const user = await this.userService.create(registerDto);
        return this.generateToken(user);
    }

    async login(loginDto: LoginDto): Promise<{access_token: string}>{
        const user = await this.validateUser(loginDto);
        return this.generateToken(user);
    }

    private async validateUser(loginDto: LoginDto): Promise<User>{
        const user = await this.userService.findByTelegramId(loginDto.telegramId);

        if(!user || !(await user.comparePassword(loginDto.password))){
            throw new UnauthorizedException("Invalid credentials");
        }

        return user;
    }

    async validateUserByPayload(payload: any): Promise<User> {
        return this.userService.findOne(payload.sub);
    }

    private generateToken(user: User): {access_token: string}{
        const payload = {telegramId: user.telegramId, sub: user.id}
        return {
            access_token: this.jwrService.sign(payload),
        };
    }
}